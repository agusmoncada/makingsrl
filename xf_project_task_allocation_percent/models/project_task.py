from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    assignment_units = fields.Integer(
        string='Assignment Units',
        default=100,
        tracking=True,
        help='The field show resource allocation percentage of the employee assigned to the task',
    )

    _sql_constraints = [
        ('check_assignment_units', 'CHECK(assignment_units >= 0 AND assignment_units <= 100)',
         'The Assignment Units should be between 0 and 100.')
    ]

    @api.constrains('assignment_units', 'stage_id', 'users_ids')
    def _check_assignment_units(self):
        error_msg = _('Total percent allocation for %s is %s%%.')
        max_percent = _('Maximum allowed percentage is %s.')
        suggestion = _('Please decrease assignment units or suspend other open tasks.')
        for task in self:
            max_percent_allocation = task.stage_id.max_percent_allocation
            if not max_percent_allocation:
                # Skip checking if value of max_percent_allocation is not set
                continue
            for user in task.user_ids:
                parallel_tasks = self.search([('user_ids', 'in', user.id), ('stage_id', '=', task.stage_id.id)])
                percent_allocation = sum(parallel_tasks.mapped('assignment_units'))
                if percent_allocation > max_percent_allocation:
                    raise ValidationError(
                        (error_msg % (user.name, percent_allocation)) + ' ' +
                        (max_percent % max_percent_allocation) + ' ' +
                        suggestion
                    )
