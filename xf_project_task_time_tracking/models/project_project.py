from odoo import models, fields


class Project(models.Model):
    _inherit = 'project.project'

    allow_time_tracking = fields.Boolean(
        string='Allow Time Tracking',
        default=True,
    )
    allow_manual_time_tracking = fields.Boolean(
        string='Allow Manual Time Tracking',
        default=False,
    )
