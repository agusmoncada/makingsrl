from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MKGWeSend(models.Model):
    _name = 'mkg.we.send'
    _description = 'Making We Send'

    name = fields.Char(string='Name', required=True, default="remito")
    invoice_number = fields.Char(string='Invoice Number')
    invoice_number_selector = fields.Many2one('account.move', string="Invoice")
    description = fields.Char(string='Description', default=lambda self: self._default_description())
    task_ids = fields.Many2many('project.task', string='Tasks')

    @api.model
    def _default_description(self):
        sequence = self.env['ir.sequence'].search([('code', '=', 'mkg.we.send.description')], limit=1)
        if sequence:
            next_number = sequence.number_next_actual or 'New'
            sequence_number = int(next_number)
            
            if sequence.min_range <= sequence_number <= sequence.max_range:
                return next_number
            else:
                raise ValidationError(f"El número de secuencia {sequence_number} está fuera del rango configurado ({sequence.min_range} - {sequence.max_range}).")
        return 'New'

    # @api.model # esto se anula porque ya se llama a _default_description en la definicion del campo
    # def create(self, vals):
    #     if 'description' not in vals or not vals['description']:
    #         vals['description'] = self._default_description()
    #     return super(MKGWeSend, self).create(vals)
    
    @api.model
    def create(self, vals):
        # Creamos el registro y capturamos la excepción si falla
        try:
            new_record = super(MKGWeSend, self).create(vals)
        except Exception as e:
            new_record = False
            # Aquí puedes manejar la excepción o simplemente pasarla
            raise e

        # Si el registro se creó correctamente, generamos la secuencia
        if new_record:
            sequence = self.env['ir.sequence'].next_by_code('mkg.we.send.description') or 'New'
            new_record.name = sequence

        return new_record


class ProjectTaskExtension(models.Model):
    _inherit = 'project.task'

    mkg_we_send_ids = fields.Many2many('mkg.we.send', string='Remitos Asociados')

class AccountInvoiceExtension(models.Model):
    _inherit = 'account.move'

    mkg_we_send_ids = fields.Many2many('mkg.we.send', string='Remitos Asociados')

class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    min_range = fields.Integer(string="Minimum Range", default=1)
    max_range = fields.Integer(string="Maximum Range", default=1000)

    @api.constrains('min_range', 'max_range')
    def _check_ranges(self):
        for record in self:
            if record.min_range >= record.max_range:
                raise ValidationError("Minimum range must be less than maximum range.")
