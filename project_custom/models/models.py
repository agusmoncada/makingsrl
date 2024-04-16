from odoo import models, fields, api

class ProjectTask(models.Model):
    _inherit = 'project.task'

    mkg_priority = fields.Selection([
        ('urgent', '1. Urgent'),
        ('high', '2. High'),
        ('half', '3. Half'),
        ('low', '4. Low'),
    ], string='Priority', default='')

    mkg_first_operator1 = fields.Many2one(
        'hr.employee', 
        string='First Operator1',
        domain=[('department_id.name', '=', 'Operaciones')]
    )

    mkg_first_operator2 = fields.Many2one(
        'hr.employee', 
        string='First Operator2',
        domain=[('department_id.name', '=', 'Operaciones')]
    )

    mkg_first_operator3 = fields.Many2one(
        'hr.employee', 
        string='First Operator3',
        domain=[('department_id.name', '=', 'Operaciones')]
    )

    mkg_first_operator4 = fields.Many2one(
        'hr.employee', 
        string='First Operator4',
        domain=[('department_id.name', '=', 'Operaciones')]
    )
    technical_report = fields.Many2one(
        'hr.employee', 
        string='Technical Report',
        domain=[('department_id.name', '=', 'Informe')]
    )

    observed = fields.Boolean(string="Observed", default=False)
    sent_to_billing = fields.Boolean(string="Sent to billing", default=False)
    delivered_to_quality = fields.Boolean(string="Delivered to quality", default=False)
    received_in_quality = fields.Boolean(string="Received in quality", default=False)
    compliant_quality = fields.Boolean(string="Compliant Quality", default=False)

    name = fields.Char(default="New")

    @api.model
    def create(self, vals):
        record = super(ProjectTask, self).create(vals)
        if record.project_id.name == 'OP. MAKING' and record.stage_id.name == 'INGRESO DE PIEZAS':
            record.write({'name': self.env['ir.sequence'].next_by_code('ot_name_general')})
        if record.project_id.name == 'OP. RKMN' and record.stage_id.name == 'GENERACIÓN OT':
            record.write({'name': self.env['ir.sequence'].next_by_code('ot_name_rak')})
        return record