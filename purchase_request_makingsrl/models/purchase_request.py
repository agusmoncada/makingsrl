from odoo import models, fields


class PurchaseRequest(models.Model):
    _inherit = "purchase.request"

    category = fields.Char('Category')