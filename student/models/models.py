# -*- coding: utf-8 -*-

from odoo import fields, models

class Student(models.Model):
    _name = 'wb.student'
    _description = 'This is student profile.'

    name = fields.Char(string='Name')
    # a = fields.Char(string='a')
    tipo = fields.Char(string='Tipo')
    fig = fields.Char(string='Fig')
    diametro = fields.Char(string='Diametro')
    marca = fields.Char(string='Marca')
    # figura = fields.Char(string='Figura')
    descripcion_opcional = fields.Text("Descripcion Opcional")
    detail_ids = fields.Many2many('wb.detail', string='Details')
    image = fields.Binary("Image", attachment=True)
    second_image = fields.Binary("Second Image", attachment=True)

    # Campos de letra del abecedario
    letra_a = fields.Char(string='A')
    letra_b = fields.Char(string='B')
    letra_c = fields.Char(string='C')
    letra_d = fields.Char(string='D')
    letra_e = fields.Char(string='E')
    letra_f = fields.Char(string='F')
    letra_g = fields.Char(string='G')
    letra_h = fields.Char(string='H')
    letra_i = fields.Char(string='I')
    letra_j = fields.Char(string='J')
    letra_k = fields.Char(string='K')
    letra_l = fields.Char(string='L')
    letra_m = fields.Char(string='M')
    letra_n = fields.Char(string='N')
    letra_o = fields.Char(string='O')
    letra_p = fields.Char(string='P')
    letra_q = fields.Char(string='Q')
    letra_r = fields.Char(string='R')
    letra_s = fields.Char(string='S')
    letra_t = fields.Char(string='T')
    letra_u = fields.Char(string='U')
    letra_v = fields.Char(string='V')
    letra_w = fields.Char(string='W')
    letra_x = fields.Char(string='X')
    letra_y = fields.Char(string='Y')
    letra_z = fields.Char(string='Z')

class WbDetail(models.Model):
    _name = 'wb.detail'
    _description = 'Detail'

    name = fields.Char("Name")
    description = fields.Text("Description")

    