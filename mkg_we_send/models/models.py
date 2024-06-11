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
    client_id = fields.Many2one('res.partner', string='Client', compute='_compute_client_id', store=True)
    state = fields.Selection([
        ('draft', 'Para Facturar'),
        ('invoiced', 'Facturado'),
        ('lost', 'Perdido'),
        ('cancelled', 'Anulado'),
    ], string='Estado', default='draft', readonly=True, copy=False, tracking=True)

    @api.onchange('invoice_number_selector')
    def _compute_state(self):
        for record in self:
            record.state = 'invoiced' if record.invoice_number_selector else 'draft'

    def action_view_selected_invoice(self):
        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.invoice_number_selector.id,
        }
        return action
    
    @api.depends('task_ids.partner_id')
    def _compute_client_id(self):
        for record in self:
            if record.task_ids:
                record.client_id = record.task_ids[0].partner_id
            else:
                record.client_id = False

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
    
    @api.model
    def default_get(self, fields_list):
        res = super(MKGWeSend, self).default_get(fields_list)
        if self.env.context.get('default_invoice_number_selector'):
            res['invoice_number_selector'] = self.env.context.get('default_invoice_number_selector')
        return res
    
    # @api.onchange('invoice_number_selector')
    # def _onchange_invoice_number_selector(self):
    #     if self.invoice_number_selector and not self.invoice_number_selector.id:
    #         self.invoice_number_selector.id = self.env.context.get('default_invoice_number_selector')

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

    def write(self, vals):
        result = super(AccountInvoiceExtension, self).write(vals)
        if 'mkg_we_send_ids' in vals:
            for move in self:
                for we_send in move.mkg_we_send_ids:
                    if not we_send.invoice_number_selector:
                        we_send.invoice_number_selector = move.id
        return result

class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    min_range = fields.Integer(string="Minimum Range", default=1)
    max_range = fields.Integer(string="Maximum Range", default=1000)

    @api.constrains('min_range', 'max_range')
    def _check_ranges(self):
        for record in self:
            if record.min_range >= record.max_range:
                raise ValidationError("Minimum range must be less than maximum range.")
