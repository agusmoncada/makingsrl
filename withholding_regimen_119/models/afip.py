# -*- coding: utf-8 -*-
from odoo import models, fields


class AfipTablagananciasEscala(models.Model):
    _inherit = 'afip.tabla_ganancias.escala'
    _rec_name = 'importe_desde'

    codigo_de_regimen = fields.Char(
        'Codigo de Regimen'
    )


class AfipTablagananciasAlicuotasymontos(models.Model):
    _name = 'afip.tabla_ganancias.alicuotasymontos'
    _rec_name = 'codigo_de_regimen'

    codigo_de_regimen = fields.Char(
        'Codigo de regimen',
        size=6,
        required=True,
        help='Codigo de regimen de inscripcion en impuesto a las ganancias.'
    )
    anexo_referencia = fields.Char(
        required=True,
    )
    concepto_referencia = fields.Text(
        required=True,
    )
    porcentaje_inscripto = fields.Float(
        '% Inscripto',
        help='Elija -1 si se debe calcular s/escala'
    )
    porcentaje_no_inscripto = fields.Float(
        '% No Inscripto'
    )
    montos_no_sujetos_a_retencion = fields.Float(
    )
