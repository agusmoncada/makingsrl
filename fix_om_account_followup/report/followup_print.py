# -*- coding: utf-8 -*-
from odoo import models
from datetime import datetime


class ReportFollowup(models.AbstractModel):
    _inherit = 'report.om_account_followup.report_followup'

    def _lines_get_with_partner(self, partner, company_id):
        res = super()._lines_get_with_partner(partner, company_id)
        for _data in res:
            _lines = _data['line']
            for line in _lines:
                date_obj = datetime.strptime(line.get('date_maturity'), '%d/%m/%Y')
                line.update({'delay_days': (datetime.now() - date_obj).days})
            _data['line'] = _lines
        return res
            
