from datetime import timedelta

from odoo import models, fields, api, _
from odoo.addons.xf_project_task_internal_state.models.internal_state import OPEN
from odoo.exceptions import ValidationError, AccessError
from pytz import utc


class ProjectTaskTimeEntry(models.Model):
    _name = 'project.task.time.entry'
    _description = 'Task Time Entry'
    _order = 'date_start asc'

    task_id = fields.Many2one(
        string='Task',
        comodel_name='project.task',
        required=True,
        ondelete='cascade',
    )
    name = fields.Char(
        string='Entry',
        required=True,
    )
    user_id = fields.Many2one(
        string='User',
        comodel_name='res.users',
        required=True,
        default=lambda self: self.env.user,
    )
    assignment_units = fields.Integer(
        string='Assignment Units',
        default=100,
        tracking=True,
        help='The field show resource allocation percentage of the employee assigned to the task',
    )
    date_start = fields.Datetime(
        string='From',
        required=True,
    )
    date_stop = fields.Datetime(
        string='To',
    )
    duration = fields.Float(
        string='Duration',
        compute='_compute_duration',
        store=True,
        help='Duration of Time Entry in Hours',
    )
    effective_hours_spent = fields.Float(
        string='Hours Spent (Effective)',
        compute='_compute_effective_hours',
        store=True,
        help='''
        Actual productive time that a person has spent on a task or activity. 
        It takes into account the time when the person was actively engaged 
        in performing the task and excludes any non-productive or idle time.
        '''
    )

    _sql_constraints = [
        (
            '_time_entry_check_date_start',
            'check (date_start IS NOT NULL)',
            'Task time entry must have start. Please define a start date.'
        ),
        (
            '_time_entry_check_start_before_stop',
            'check (date_stop > date_start)',
            'Starting time should be before end time.'
        ),
        (
            '_time_entry_no_overlap',
            """
            EXCLUDE USING GIST (
                tsrange(date_start, date_stop, '()') WITH &&,
                int4range(user_id, user_id, '[]') WITH =,
                int4range(task_id, task_id, '[]') WITH = 
            )
            WHERE (date_start IS NOT NULL AND date_stop IS NOT NULL)
            """,
            'Task time entries cannot overlap'
        ),
    ]

    @api.depends('date_start', 'date_stop', 'assignment_units')
    def _compute_duration(self):
        for entry in self:
            date_start = entry.date_start
            date_stop = entry.date_stop
            duration = 0.0
            if date_start and date_stop:
                dt = date_stop - date_start
                duration = dt.total_seconds() / 3600  # Number of hours

            entry.duration = duration

    @api.depends('user_id', 'assignment_units', 'date_start', 'date_stop')
    def _compute_effective_hours(self):
        for entry in self:
            if not entry.assignment_units or not entry.user_id or not entry.date_start:
                entry.effective_hours_spent = 0
                continue
            date_start = entry.date_start
            date_stop = entry.date_stop
            if not date_stop:
                date_stop = fields.Datetime.now()
            calendar = self.env['resource.calendar']
            user = entry.user_id
            if hasattr(user, 'employee_resource_calendar_id'):
                calendar = getattr(user, 'employee_resource_calendar_id')
            if not calendar:
                calendar = user.resource_calendar_id
            if not calendar or not user.resource_ids:
                entry.effective_hours_spent = 0
                continue
            intervals = calendar._work_intervals_batch(
                date_start.replace(tzinfo=utc),
                date_stop.replace(tzinfo=utc),
                user.resource_ids
            )
            spent_hours = 0
            for resource in user.resource_ids:
                spent_hours += sum(
                    (stop - start).total_seconds() / 3600
                    for start, stop, meta in intervals[resource.id]
                )
            entry.effective_hours_spent = spent_hours * (entry.assignment_units / 100)

    def check_access_rule(self, operation):
        self._check_manual_time_tracking(operation)
        return super(ProjectTaskTimeEntry, self).check_access_rule(operation)

    def _check_manual_time_tracking(self, operation):
        if not self.env.context.get('auto_time_tracking') and operation != 'read':
            for entry in self:
                if not entry.task_id.allow_manual_time_tracking:
                    raise AccessError(_('Manual editing of time entries is disabled!'))

    def _recompute_effective_hours_spent_cron(self):
        self.search([('date_stop', '=', False)])._compute_effective_hours()


class ProjectTask(models.Model):
    _inherit = 'project.task'

    allow_time_tracking = fields.Boolean(
        string='Allow Time Tracking',
        related='project_id.allow_time_tracking',
    )
    allow_manual_time_tracking = fields.Boolean(
        string='Allow Manual Time Tracking',
        related='project_id.allow_manual_time_tracking',
    )
    time_entry_ids = fields.One2many(
        string='Time Entries',
        comodel_name='project.task.time.entry',
        inverse_name='task_id',
    )
    is_in_progress = fields.Boolean(
        string='Is Task in Progress',
        compute='_compute_is_in_progress',
    )
    sum_tracked_duration = fields.Float(
        string='Tracked Duration',
        compute='_sum_tracked_duration',
        store=True,
    )
    sum_tracked_effective_hours_spent = fields.Float(
        string='Tracked Effective Hours',
        compute='_sum_tracked_effective_hours_spent',
        store=True,
    )

    @api.depends('internal_state', 'kanban_state')
    def _compute_is_in_progress(self):
        for task in self:
            task.is_in_progress = task.internal_state == OPEN and task.kanban_state == 'normal'

    @api.depends('time_entry_ids.effective_hours_spent')
    def _sum_tracked_effective_hours_spent(self):
        for task in self:
            task.sum_tracked_effective_hours_spent = sum(task.time_entry_ids.mapped('effective_hours_spent'))

    @api.depends('time_entry_ids.duration')
    def _sum_tracked_duration(self):
        for task in self:
            task.sum_tracked_duration = sum(task.time_entry_ids.mapped('duration'))

    def _track_subtype(self, init_values):
        self.update_time_entries(init_values)
        return super(ProjectTask, self)._track_subtype(init_values)

    @api.constrains('user_ids', 'stage_id', 'kanban_state')
    def _check_assignees(self):
        for task in self:
            if task.is_in_progress and not task.user_ids:
                raise ValidationError(_("The task cannot be started until it's assigned to someone."))

    def update_time_entries(self, init_values):
        if not self.allow_time_tracking:
            return
        close_timesheet = False
        create_timesheet = False

        create_description = None
        close_description = None

        # Check if task kanban state is changed
        if 'kanban_state_label' in init_values and self.kanban_state_label != init_values.get('kanban_state_label'):
            create_description = close_description = self.kanban_state_label
            # Close existing timesheet if kanban state is done or blocked
            close_timesheet = self.kanban_state in ('done', 'blocked')
            # Create new timesheet if internal state is open and kanban state is normal
            create_timesheet = self.is_in_progress

        # Check if task stage is changed
        if 'stage_id' in init_values and self.stage_id != init_values.get('stage_id'):
            create_description = close_description = self.stage_id.display_name
            # Close existing timesheet if task stage is changed
            close_timesheet = True
            # Create new timesheet if internal state is open and kanban state is normal
            create_timesheet = self.is_in_progress

        # Check if task assignees are changed
        if 'user_ids' in init_values and init_values.get('user_ids') and self.user_ids != init_values.get('user_ids'):
            # If user is changed and internal state is open
            create_description = self.stage_id.display_name
            close_description = 'Reassigning Task'
            # Close existing timesheet if assigned user is changed
            close_timesheet = True
            # Create new timesheet if internal state is open and kanban state is normal
            create_timesheet = self.is_in_progress

        # Check if the "assignment units" value is changed
        if 'assignment_units' in init_values and init_values.get('assignment_units') != self.assignment_units:
            create_description = self.stage_id.display_name
            close_description = None
            close_timesheet = True
            create_timesheet = self.is_in_progress

        if close_timesheet:
            self.close_time_entry(close_description)
        if create_timesheet:
            self.create_time_entry(create_description)

    def create_time_entry(self, description):
        for task in self:
            if not task.is_in_progress or not task.user_ids:
                # Do not track if task is not in progress or is not assigned
                continue
            if self.env.uid not in task.user_ids.ids:
                # Track time only for assigned users
                continue

            self.env['project.task.time.entry'].with_context(auto_time_tracking=True).create({
                'name': description,
                'task_id': task.id,
                'user_id': self.env.uid,
                'date_start': fields.Datetime.now() + timedelta(seconds=1),
                'assignment_units': task.assignment_units,
            })

    def close_time_entry(self, description=None):
        for task in self:
            domain = [('task_id', '=', task.id), ('date_stop', '=', False)]
            unclosed_entry = self.env['project.task.time.entry'].search(domain, order='date_start desc', limit=1)
            if unclosed_entry:
                vals = {
                    'date_stop': fields.Datetime.now(),
                }
                if description:
                    vals['name'] = f'{unclosed_entry.name} -> {description}'
                unclosed_entry.with_context(auto_time_tracking=True).write(vals)
