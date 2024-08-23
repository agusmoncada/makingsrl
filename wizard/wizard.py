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









'''import base64
import xlsxwriter
from io import BytesIO
from odoo import api, fields, models
import logging
import json

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
        _logger.info('Grupos de pagos encontrados: %s', len(payment_groups))
        
        # Filtra las facturas en base a las fechas seleccionadas
        invoices = self.env['account.move'].search([
            ('state', '=', 'posted'),
            ('move_type', 'in', ['out_invoice', 'out_refund']),
            ('invoice_date', '>=', self.date_from),
            ('invoice_date', '<=', self.date_to)
        ])
        _logger.info('FACTURAS ENCONTRADAS: %s', len(invoices))
        _logger.debug('Detalles de las facturas encontradas: %s', invoices.mapped(lambda inv: inv.id))


        report_data = []

        # Procesa las facturas para obtener percepciones
        for invoice in invoices:
            _logger.info('PROCESA LAS FACURAS PARA OBTENER PERCEPCION')
            # Accede directamente a tax_totals, ya que es un dict
            _logger.info('accediendo a taxtotals')
            _logger.info('Contenido de tax_totals: %s', invoice.tax_totals)
            taxes = invoice.tax_totals.get('groups_by_subtotal', {}).get('Importe sin impuestos', [])
            for tax in taxes:
                _logger.info('Contenido de tax: %s', tax)
                _logger.info('Valor de tax_group_name: %s', tax.get('tax_group_name', ''))
                if 'Per' in tax.get('tax_group_name', ''):
                    data = [
                        invoice.invoice_date,  # Fecha
                        tax.get('tax_group_name', ''),  # Retención Ganancia
                        invoice.partner_id.name,  # Partner ID
                        invoice.partner_id.vat,  # CUIT
                        tax.get('tax_group_amount', 0.0),  # Monto Retención
                        invoice.amount_total  # Monto Total
                    ]
                    report_data.append(data)
                    _logger.debug('Datos añadidos para la factura %s: %s', invoice.id, data)


        # Procesa los grupos de pagos para obtener retenciones
        _logger.info('Número de grupos de pagos a procesar: %s', len(payment_groups))
        for payment_group in payment_groups:
            try:
                _logger.debug('Procesando grupo de pagos ID: %s', payment_group.id)
                _logger.debug('Número de líneas en el grupo de pagos %s: %s', payment_group.id, len(payment_group.move_line_ids))
                for line in payment_group.move_line_ids:
                    _logger.debug('Línea de movimiento ID: %s', line.id)
                    _logger.debug('Tax Line ID: %s', line.tax_line_id.id if line.tax_line_id else 'No tax line')
                    if line.tax_line_id:
                        _logger.debug('Datos de la línea con tax_line_id: %s', {
                            'payment_date': payment_group.payment_date,
                            'tax_line_name': line.tax_line_id.name,
                            'partner_name': payment_group.partner_id.name,
                            'partner_vat': payment_group.partner_id.vat,
                            'debit_or_credit': line.debit or line.credit,
                            'payment_amount': payment_group.amount
                        })
                        data = [
                            payment_group.payment_date,  # Fecha
                            line.tax_line_id.name,  # Retención Ganancia
                            payment_group.partner_id.name,  # Partner ID
                            payment_group.partner_id.vat,  # CUIT
                            line.debit or line.credit,  # Monto Retención
                            payment_group.amount  # Monto Total
                        ]
                        report_data.append(data)
                        _logger.debug('Datos añadidos para el grupo de pagos %s: %s', payment_group.id, data)
            except Exception as e:
                _logger.error('Error procesando grupo de pagos ID %s: %s', payment_group.id, str(e))



        # Crea un archivo Excel y lo guarda en un buffer
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        # Define el formato de la cabecera
        header_format = workbook.add_format({'bold': True, 'bg_color': 'yellow'})
        columns = ['Fecha', 'Retención Ganancia', 'Partner ID', 'CUIT', 'Monto Retención', 'Monto Total']

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
'''
