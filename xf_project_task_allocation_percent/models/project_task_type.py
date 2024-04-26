from odoo import models, fields, api


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    max_percent_allocation = fields.Integer(
        string='Max Percent Allocation per Employee',
        default=0,
        help='''
        Maximum Percent Allocation field contains the percentage that represents 
        the total amount of a resource's capacity can be allocated to tasks by one employee.
        '''
    )
