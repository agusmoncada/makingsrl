# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountTax(models.Model):
    _inherit = "account.tax"

    def get_withholding_vals(self, payment):
        commercial_partner = payment.commercial_partner_id

        force_withholding_amount_type = None
        if self.withholding_type == 'partner_tax':
            alicuot_line = self.get_partner_alicuot(
                commercial_partner,
                payment.date or fields.Date.context_today(self),
            )
            alicuota = alicuot_line.alicuota_retencion / 100.0
            force_withholding_amount_type = alicuot_line.withholding_amount_type

        vals = super(AccountTax, self).get_withholding_vals(payment)
        base_amount = vals['withholdable_base_amount']

        if self.withholding_type == 'partner_tax':
            amount = base_amount * (alicuota)
            vals['comment'] = "%s x %s" % (
                base_amount, alicuota)
            vals['period_withholding_amount'] = amount
        elif self.withholding_type == 'tabla_ganancias':
            regimen = payment.regimen_ganancias_id
            imp_ganancias_padron = commercial_partner.imp_ganancias_padron
            if (
                    payment.retencion_ganancias != 'nro_regimen' or
                    not regimen):
                # if amount zero then we dont create withholding
                amount = 0.0
            elif not imp_ganancias_padron:
                raise UserError(_(
                    'El partner %s no tiene configurada inscripcion en '
                    'impuesto a las ganancias' % commercial_partner.name))
            elif imp_ganancias_padron in ['EX', 'NC']:
                # if amount zero then we dont create withholding
                amount = 0.0
            # TODO validar excencion actualizada
            elif imp_ganancias_padron == 'AC':
                # alicuota inscripto
                non_taxable_amount = (
                    regimen.montos_no_sujetos_a_retencion)
                vals['withholding_non_taxable_amount'] = non_taxable_amount
                if base_amount < non_taxable_amount:
                    base_amount = 0.0
                else:
                    base_amount -= non_taxable_amount
                vals['withholdable_base_amount'] = base_amount
                if regimen.porcentaje_inscripto == -1:
                    # hacemos <= porque si es 0 necesitamos que encuentre
                    # la primer regla (0 es en el caso en que la no
                    # imponible sea mayor)
                    codigo_de_regimen = '119' if regimen.codigo_de_regimen == '119' else False
                    escala = self.env['afip.tabla_ganancias.escala'].search([
                        ('importe_desde', '<=', base_amount),
                        ('importe_hasta', '>', base_amount),
                        ('codigo_de_regimen', '=', codigo_de_regimen)
                    ], limit=1)
                    if not escala:
                        raise UserError(
                            'No se encontro ninguna escala para el monto'
                            ' %s' % (base_amount))
                    amount = escala.importe_fijo
                    amount += (escala.porcentaje / 100.0) * (
                        base_amount - escala.importe_excedente)
                    vals['comment'] = "%s + (%s x %s)" % (
                        escala.importe_fijo,
                        base_amount - escala.importe_excedente,
                        escala.porcentaje / 100.0)
                else:
                    amount = base_amount * (
                        regimen.porcentaje_inscripto / 100.0)
                    vals['comment'] = "%s x %s" % (
                        base_amount, regimen.porcentaje_inscripto / 100.0)
            elif imp_ganancias_padron == 'NI':
                # alicuota no inscripto
                amount = base_amount * (
                    regimen.porcentaje_no_inscripto / 100.0)
                vals['comment'] = "%s x %s" % (
                    base_amount, regimen.porcentaje_no_inscripto / 100.0)
            # TODO, tal vez sea mejor utilizar otro campo?
            vals['ref'] = "%s - %s" % (regimen.codigo_de_regimen, regimen.concepto_referencia)
            vals['period_withholding_amount'] = amount
        return vals
