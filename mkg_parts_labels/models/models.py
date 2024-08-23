from odoo import models, fields

class MKGPartsLabels(models.Model):
    _name = 'mkg.parts.labels'
    _description = 'Making Parts Labels'

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description', required=True)

class PiezasExtension(models.Model):
    _inherit = 'wb.student'

    mkg_parts_labels_id = fields.Many2many('mkg.parts.labels', string='Making Parts Labels', help='Select the Making Parts Labels.')
