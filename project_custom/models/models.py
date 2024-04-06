from odoo import models, fields

class ProjectTask(models.Model):
    _inherit = 'project.task'

    mkg_priority = fields.Selection([
        ('urgent', '1. Urgent'),
        ('high', '2. High'),
        ('half', '3. Half'),
        ('low', '4. Low'),
    ], string='Priority', default='half')

    mkg_first_operator1 = fields.Many2one(
        'hr.employee', 
        string='First Operator1',
        domain=[('job_id.name', '=', 'Operador')]
    )

    mkg_first_operator2 = fields.Many2one(
        'hr.employee', 
        string='First Operator2',
        domain=[('job_id.name', '=', 'Operador')]
    )

    mkg_first_operator3 = fields.Many2one(
        'hr.employee', 
        string='First Operator3',
        domain=[('job_id.name', '=', 'Operador')]
    )

    mkg_first_operator4 = fields.Many2one(
        'hr.employee', 
        string='First Operator4',
        domain=[('job_id.name', '=', 'Operador')]
    )
    technical_report = fields.Many2one(
        'hr.employee', 
        string='Technical Report',
        domain=[('job_id.name', '=', 'Informes')]
    )

    observed = fields.Boolean(string="Observed", default=False)
    sent_to_billing = fields.Boolean(string="Sent to billing", default=False)
    delivered_to_quality = fields.Boolean(string="Delivered to quality", default=False)
    received_in_quality = fields.Boolean(string="Received in quality", default=False)
    compliant_quality = fields.Boolean(string="Compliant Quality", default=False)