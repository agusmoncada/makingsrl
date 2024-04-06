from odoo import models, fields, api

from .internal_state import INTERNAL_STATES_SELECTION, INTERNAL_STATES


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    internal_state = fields.Selection(
        string='Internal State',
        selection=INTERNAL_STATES_SELECTION,
        help='Internal states for tasks to facilitate the easy determination of task statuses',
    )


class ProjectTask(models.Model):
    _inherit = 'project.task'

    internal_state = fields.Selection(
        related='stage_id.internal_state',
        store=True,
        readonly=True,
        help='Internal states for tasks to facilitate the easy determination of task statuses',
    )

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        """ Override read_group to always display all states. """
        if groupby and groupby[0] == 'internal_state' and 'kanban_state' not in groupby:
            return self._read_group_by_internal_state(domain)
        else:
            return super(ProjectTask, self).read_group(domain, fields, groupby, offset, limit, orderby, lazy)

    def _read_group_by_internal_state(self, domain):
        result = []
        for state, label in INTERNAL_STATES.items():
            internal_state_domain = domain + [('internal_state', '=', state)]
            result.append({
                'internal_state': (state, label),
                'internal_state_count': self.search_count(internal_state_domain),
                '__domain': internal_state_domain,
                '__fold': False,
            })
        return result
