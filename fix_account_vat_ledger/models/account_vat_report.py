# -*- coding: utf-8 -*-
##############################################################################
from odoo import models, api


class AccountVatLedger(models.Model):
    _inherit = "account.vat.ledger"

    @api.onchange('journal_ids', 'period_id')
    def _get_data(self):
        return super()._get_data()

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res._get_data()
        return res


