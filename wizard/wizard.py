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
        payment_groups = self.env['account.payment.group'].sudo().search([
            ('state', '=', 'posted'),
            ('payment_date', '>=', self.date_from),
            ('payment_date', '<=', self.date_to),
        ])
        _logger.info('Número de grupos de pagos encontrados: %s', len(payment_groups))
        _logger.info('Contenido de payment_groups: %s', payment_groups)

        report_data = []

        for payment_group in payment_groups:
            try:
                _logger.info('Procesando grupo de pagos ID: %s', payment_group.id)
                _logger.info('Fecha de pago del grupo: %s', payment_group.payment_date)
                _logger.info('Partner del grupo de pagos: %s (%s)', payment_group.partner_id.name, payment_group.partner_id.vat)
                _logger.info('Número de pagos en el grupo de pagos %s: %s', payment_group.id, len(payment_group.payment_ids))

                for payment in payment_group.payment_ids:
                    _logger.info('Línea de pago ID: %s', payment.id)
                    _logger.info('Tax Withholding ID: %s', payment.tax_withholding_id.id if payment.tax_withholding_id else 'No tax withholding')

                    if payment.tax_withholding_id:
                        data = [
                            payment_group.regimen_ganancias_id.codigo_de_regimen if payment_group.regimen_ganancias_id else 'No régimen',  # Retención Ganancia
                            payment_group.payment_date,  # Fecha
                            payment_group.partner_id.name,  # Partner ID
                            payment_group.partner_id.vat,  # CUIT
                            payment.signed_amount,  # Monto Retención
                            payment_group.payments_amount,  # Monto Total
                            payment_group.display_name #Numero de operacion
                        ]
                        report_data.append(data)
                        _logger.info('Datos añadidos para el grupo de pagos %s: %s', payment_group.id, data)
            except Exception as e:
                _logger.error('Error procesando grupo de pagos ID %s: %s', payment_group.id, str(e))



       # Crea un archivo Excel y lo guarda en un buffer
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Define el formato de la cabecera
        header_format = workbook.add_format({'bold': True, 'bg_color': 'yellow'})
        columns = ['Régimen','Fecha', 'Proveedor', 'CUIT', 'Monto Retención', 'Monto Total', 'Nro. OP']

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



