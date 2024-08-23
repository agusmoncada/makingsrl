import base64
import xlsxwriter
from io import BytesIO
from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class RetencionGananciasWizard(models.TransientModel):
    _name = "retencion.ganancias.wizard"
    _description = "Wizard para generar reporte de retenciones"

    date_from = fields.Date(string="Fecha Inicio", required=True)
    date_to = fields.Date(string="Fecha Fin", required=True)

    def print_report(self):
        _logger.info('Iniciando la generación del reporte.')
        # Filtra los grupos de pagos en base a las fechas seleccionadas
        payment_groups = self.env['account.payment.group'].search([
            ('state', '=', 'posted'),
            ('payment_date', '>=', self.date_from),
            ('payment_date', '<=', self.date_to),
        ])
        _logger.info('Grupos de pagos encontrados: %s', len(payment_groups))

        # Inicializa listas para los datos que se exportarán
        report_data = []

        # Procesa los grupos de pagos para obtener la información necesaria
        for payment_group in payment_groups:
            _logger.debug('Procesando grupo de pagos: %s', payment_group.name)
            for line in payment_group.move_line_ids:
                _logger.debug('Procesando línea: %s', line.id)
                if line.tax_line_id:
                    data = []
                    data.append(line.tax_line_id.name)  # Regimen
                    data.append(payment_group.payment_date)  # Fecha retención
                    data.append(payment_group.partner_id.name)  # Proveedor
                    data.append(payment_group.partner_id.vat)  # CUIT proveedor
                    data.append(line.debit or line.credit)  # Monto retención
                    data.append(payment_group.amount)  # Monto total
                    data.append(payment_group.name)  # Número OP
                    _logger.debug('Datos recolectados: %s', data)
                    report_data.append(data)

        # Crea un archivo Excel y lo guarda en un buffer
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Define el formato de la cabecera
        header_format = workbook.add_format({'bold': True, 'bg_color': 'yellow'})
        columns = ['Regimen', 'Fecha Retención', 'Proveedor', 'CUIT Proveedor', 'Monto Retención', 'Monto Total', 'Número OP']

        for col, header in enumerate(columns):
            worksheet.write(0, col, header, header_format)

        # Llena los datos
        for row, data in enumerate(report_data, start=1):
            for col, value in enumerate(data):
                worksheet.write(row, col, value)

        workbook.close()
        output.seek(0)

        # Retorna el archivo Excel como un archivo adjunto
        attachment = self.env['ir.attachment'].create({
            'name': 'Reporte_Retenciones.xlsx',
            'type': 'binary',
            'datas': base64.b64encode(output.read()),
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })
        _logger.info('Reporte generado y archivo adjunto creado con ID: %s', attachment.id)
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'self'
        }
