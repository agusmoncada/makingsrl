from odoo import models, fields

class MKGCategories(models.Model):
    _name = 'mkg.categories'
    _description = 'Making Categories'

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description', required=True)

class ProjectTaskExtension(models.Model):
    _inherit = 'project.task'

    mkg_categories_id = fields.Many2one('mkg.categories', string='Making Categories', help='Select the Making Category.')
