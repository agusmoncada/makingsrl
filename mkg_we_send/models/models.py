from odoo import models, fields, api

class MKGWeSend(models.Model):
    _name = 'mkg.we.send'
    _description = 'Making We Send'

    name = fields.Char(string='Invoice Number', required=True)
    description = fields.Char(string='Description', default=lambda self: self._default_description())
    task_ids = fields.Many2many('project.task', string='Tasks')

    @api.model
    def _default_description(self):
        return self.env['ir.sequence'].next_by_code('mkg.we.send.description') or 'New'

    @api.model
    def create(self, vals):
        if 'description' not in vals or not vals['description']:
            vals['description'] = self._default_description()
        return super(MKGWeSend, self).create(vals)


class ProjectTaskExtension(models.Model):
    _inherit = 'project.task'

    mkg_we_send_ids = fields.Many2many('mkg.we.send', string='Remitos Asociados')
