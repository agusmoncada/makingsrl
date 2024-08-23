import json
from odoo import api, fields, models

class RetencionGananciasWizard(models.TransientModel):
    _name = "retencion.ganancias.wizard"
    _description = "Wizard para generar reporte de retenciones"

    date_from = fields.Date(string="Fecha Inicio", required=True)
    date_to = fields.Date(string="Fecha Fin", required=True)

    def print_report(self):
        # Filtra las facturas en base a las fechas seleccionadas
        payments = self.env['account.payment'].search([
            ('state', '=', 'posted'),
            ('payment_date', '>=', self.date_from),
            ('payment_date', '<=', self.date_to),
        ])

        # Inicializa listas para los datos que se exportarán
        report_data = []

        # Procesa los pagos para obtener la información necesaria
        for payment in payments:
            for line in payment.line_ids:
                if line.tax_line_id:
                    data = []
                    data.append(line.tax_line_id.name)  # Regimen
                    data.append(payment.payment_date)  # Fecha retención
                    data.append(payment.partner_id.name)  # Proveedor
                    data.append(payment.partner_id.vat)  # CUIT proveedor
                    data.append(line.debit or line.credit)  # Monto retención
                    data.append(payment.amount)  # Monto total
                    data.append(payment.name)  # Número OP
                    report_data.append(data)

        # Envía los datos al reporte para generar el archivo Excel
        data = {
            'from_data': self.read()[0],
            'report_data': report_data,
        }

        return self.env.ref('report_retenciones.action_retencion_ganancias_report').sudo().with_context(landscape=True).report_action(self, data=data)



