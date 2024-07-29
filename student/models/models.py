# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import UserError

class Student(models.Model):
    _name = 'wb.student'
    _description = 'This is student profile.'

    name = fields.Char(string='Name')
    # a = fields.Char(string='a')
    tipo = fields.Char(string='Tipo')
    fig = fields.Char(string='Fig')
    diametro = fields.Char(string='Diametro')
    presion = fields.Char(string='Presion')
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

class Ingreso(models.Model):
    _name = 'ingreso'
    _description = 'ABM de ingreso de piezas'

    name = fields.Char(string='Name')
    cliente = fields.Many2one('res.partner', string='Cliente')
    fecha = fields.Date(string='Fecha')
    equipo = fields.Char(string='Equipo')
    numero_ot = fields.Many2one('project.task', string='Número de OT')
    responsable = fields.Many2many('res.users', string='Responsables')
    ubicacion = fields.Char(string='Ubicación')
    seleccionar_piezas = fields.Many2one('wb.student', string='Seleccionar Pieza')
    cantidad_piezas = fields.Integer(string='Cantidad de piezas')
    numero_serie = fields.Integer(string='Numero de Serie')
    # descripcion_larga = fields.Char(string='Descripcion Larga')
    # Campo Many2many para la relación con planilla.recepcion
    planilla_ids = fields.Many2many('planilla.recepcion', string='Planillas de Recepción')

    iv_inspeccion_visual = fields.Boolean(string='IV: Inspección Visual')
    ga_inspeccion_calibres = fields.Boolean(string='GA: Inspección con Calibres')
    me_medicion_espesores = fields.Boolean(string='ME: Medición de Espesores')
    pm_particulas_magnetizables = fields.Boolean(string='PM: Partículas Magnetizables')
    lp_liquidos_penetrantes = fields.Boolean(string='LP: Líquidos Penetrantes')
    ph_prueba_hidrostatica = fields.Boolean(string='PH: Prueba Hidrostática')
    inf_informe_final = fields.Boolean(string='INF: Informe Final')

    def generar_plantilla(self):
        # Iterar sobre cada registro de ingreso
        for ingreso in self:
            # Crear registros en planilla.recepcion según la cantidad de piezas
            for i in range(ingreso.cantidad_piezas):
                # Crear un registro nuevo en planilla.recepcion
                vals = {
                    'descripcion': ingreso.seleccionar_piezas.name,
                    'pieza_id': ingreso.seleccionar_piezas.id,
                    'serie': str(ingreso.numero_serie + i)  # Autocompletar número de serie
                }
                planilla = self.env['planilla.recepcion'].create(vals)
                # Agregar el nuevo registro a la relación Many2many
                ingreso.planilla_ids |= planilla

                # Crear un registro en formulario.prueba por cada check marcado
                if ingreso.iv_inspeccion_visual:
                    formulario = self.env['formulario.prueba.iv'].create({'name': 'IV'})
                    planilla.iv = formulario
                if ingreso.ga_inspeccion_calibres:
                    formulario = self.env['formulario.prueba.ga'].create({'name': 'GA'})
                    planilla.ga = formulario
                if ingreso.me_medicion_espesores:
                    formulario = self.env['formulario.prueba.me'].create({'name': 'ME'})
                    planilla.me = formulario
                if ingreso.pm_particulas_magnetizables:
                    formulario = self.env['formulario.prueba.pm'].create({'name': 'PM'})
                    planilla.pm = formulario
                if ingreso.lp_liquidos_penetrantes:
                    formulario = self.env['formulario.prueba.lp'].create({'name': 'LP'})
                    planilla.lp = formulario
                if ingreso.ph_prueba_hidrostatica:
                    formulario = self.env['formulario.prueba.ph'].create({'name': 'PH'})
                    planilla.ph = formulario
                if ingreso.inf_informe_final:
                    formulario = self.env['formulario.prueba.inf'].create({'name': 'INF'})
                    planilla.inf = formulario

        # Actualizar campos en el modelo Ingreso
        self.write({
            'iv_inspeccion_visual': False,
            'ga_inspeccion_calibres': False,
            'me_medicion_espesores': False,
            'pm_particulas_magnetizables': False,
            'lp_liquidos_penetrantes': False,
            'ph_prueba_hidrostatica': False,
            'inf_informe_final': False,
            'seleccionar_piezas': False,
            'cantidad_piezas': 0,
            'numero_serie': 0
        })

        return True

class PlanillaRecepcion(models.Model):
        _name = 'planilla.recepcion'
        _description = 'Planilla de Recepción e Inspección Previa de Elementos Recibidos'

        item = fields.Integer(string='Item')
        # pieza = fields.Integer(string='Pieza')
        pieza_id = fields.Many2one('wb.student', string='Pieza')
        descripcion = fields.Char(string='Descripción')
        serie = fields.Char(string='Serie')
        precinto = fields.Char(string='Nº de Precinto')
        le = fields.Many2one('formulario.prueba.le', string='LE: Limpieza Extremos', ondelete='cascade')
        iv = fields.Many2one('formulario.prueba.iv', string='IV: Inspección Visual', ondelete='cascade')
        ga = fields.Many2one('formulario.prueba.ga', string='GA: Inspección con Calibres', ondelete='cascade')
        me = fields.Many2one('formulario.prueba.me', string='ME: Medición de Espesores', ondelete='cascade')
        pm = fields.Many2one('formulario.prueba.pm', string='PM: Partículas Magnetizables', ondelete='cascade')
        lp = fields.Many2one('formulario.prueba.lp', string='LP: Líquidos Penetrantes', ondelete='cascade')
        ph = fields.Many2one('formulario.prueba.ph', string='PH: Prueba Hidrostática', ondelete='cascade')
        inf = fields.Many2one('formulario.prueba.inf', string='INF: Informe Final', ondelete='cascade')

        def open_le_form(self):
            # Buscar un registro existente en 'formulario.prueba.le' con el mismo 'planilla_id'
            existing_record = self.env['formulario.prueba.le'].search([
                ('planilla_id', '=', self.id)
            ], limit=1)

            if existing_record:
                # Si existe un registro, abrir el formulario de ese registro
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'LE: Limpieza Extremos',
                    'res_model': 'formulario.prueba.le',
                    'view_mode': 'form',
                    'res_id': existing_record.id,
                    'target': 'new',
                }
            else:
                # Si no existe un registro, crear uno nuevo y abrir el formulario
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'LE: Limpieza Extremos',
                    'res_model': 'formulario.prueba.le',
                    'view_mode': 'form',
                    'res_id': self.le.id,
                    'target': 'new',
                    'context': {
                    'default_planilla_id': self.id,
                    },
                }
            
        def open_iv_form(self):
            # Buscar un registro existente en 'formulario.prueba.iv' con el mismo 'planilla_id'
            existing_record = self.env['formulario.prueba.iv'].search([
                ('planilla_id', '=', self.id)
            ], limit=1)

            if existing_record:
                # Si existe un registro, abrir el formulario de ese registro
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'IV: Inspección Visual',
                    'res_model': 'formulario.prueba.iv',
                    'view_mode': 'form',
                    'res_id': existing_record.id,
                    'target': 'new',
                }
            else:
                # Si no existe un registro, crear uno nuevo y abrir el formulario
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'IV: Inspección Visual',
                    'res_model': 'formulario.prueba.iv',
                    'view_mode': 'form',
                    'res_id': self.iv.id,
                    'target': 'new',
                    'context': {
                    'default_planilla_id': self.id,
                    },
                }

        def open_ga_form(self):
            # Buscar un registro existente en 'formulario.prueba.le' con el mismo 'planilla_id'
            existing_record = self.env['formulario.prueba.ga'].search([
                ('planilla_id', '=', self.id)
            ], limit=1)

            if existing_record:
                # Si existe un registro, abrir el formulario de ese registro
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'GA: Inspección con Calibres',
                    'res_model': 'formulario.prueba.ga',
                    'view_mode': 'form',
                    'res_id': existing_record.id,
                    'target': 'new',
                }
            else:
                # Si no existe un registro, crear uno nuevo y abrir el formulario
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'GA: Inspección con Calibres',
                    'res_model': 'formulario.prueba.le',
                    'view_mode': 'form',
                    'res_id': self.ga.id,
                    'target': 'new',
                    'context': {
                    'default_planilla_id': self.id,
                    },
                }
        def open_me_form(self):
            # Buscar un registro existente en 'formulario.prueba.le' con el mismo 'planilla_id'
            existing_record = self.env['formulario.prueba.me'].search([
                ('planilla_id', '=', self.id)
            ], limit=1)

            if existing_record:
                # Si existe un registro, abrir el formulario de ese registro
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'ME: Medición de Espesores',
                    'res_model': 'formulario.prueba.me',
                    'view_mode': 'form',
                    'res_id': existing_record.id,
                    'target': 'new',
                    'context': {
                    'default_punto_a_minimo_admisible': self.pieza_id.letra_a,
                    'default_punto_b_minimo_admisible': self.pieza_id.letra_b,
                    },
                }
            else:
                # Si no existe un registro, crear uno nuevo y abrir el formulario
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'ME: Medición de Espesores',
                    'res_model': 'formulario.prueba.me',
                    'view_mode': 'form',
                    'res_id': self.me.id,
                    'target': 'new',
                    'context': {
                    'default_planilla_id': self.id,
                    'default_punto_a_minimo_admisible': self.pieza_id.letra_a,
                    'default_punto_b_minimo_admisible': self.pieza_id.letra_b,
                    },
                }

        def open_pm_form(self):
            # Buscar un registro existente en 'formulario.prueba.le' con el mismo 'planilla_id'
            existing_record = self.env['formulario.prueba.pm'].search([
                ('planilla_id', '=', self.id)
            ], limit=1)

            if existing_record:
                # Si existe un registro, abrir el formulario de ese registro
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'PM: Partículas Magnetizables',
                    'res_model': 'formulario.prueba.pm',
                    'view_mode': 'form',
                    'res_id': existing_record.id,
                    'target': 'new',
                }
            else:
                # Si no existe un registro, crear uno nuevo y abrir el formulario
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'PM: Partículas Magnetizables',
                    'res_model': 'formulario.prueba.pm',
                    'view_mode': 'form',
                    'res_id': self.pm.id,
                    'target': 'new',
                    'context': {
                    'default_planilla_id': self.id,
                    },
                }


class InspeccionVisual(models.Model):
    _name = 'formulario.prueba.iv'
    _description = 'IV: Inspección Visual'

    name = fields.Char(string='Nombre', related='planilla_id.descripcion', store=True)
    estado_general = fields.Boolean(string='Estado General', default=False)
    estado_rosca = fields.Boolean(string='Estado Rosca', default=False)
    corrosion = fields.Boolean(string='Corrosion', default=False)
    estado_sellos = fields.Boolean(string='Estado de los Sellos', default=False)
    observaciones = fields.Text(string='Observaciones')
    planilla_id = fields.Many2one('planilla.recepcion', string='Planilla Recepcion', ondelete='cascade')
    aprobado = fields.Boolean(string='Aprobado', default=False)

    def aprobar_y_siguiente(self):
        # Alternar el estado del campo aprobado
        self.aprobado = True
        
        # Buscar un registro en 'formulario.prueba.iv' con el mismo 'planilla_id'
        iv_record = self.env['formulario.prueba.ga'].search([
            ('planilla_id', '=', self.planilla_id.id)
        ], limit=1)

        if iv_record:
            # Si existe un registro, abrir el formulario de ese registro
            return {
                'type': 'ir.actions.act_window',
                'name': 'IV: Inspección Visual',
                'res_model': 'formulario.prueba.ga',
                'view_mode': 'form',
                # 'view_type': 'form',
                'res_id': iv_record.id,
                'target': 'new',  # Abre en la misma ventana
            }
        else:
            # Si no existe un registro, crear uno nuevo y abrir el formulario
            return {
                'type': 'ir.actions.act_window',
                'name': 'IV: Inspección Visual',
                'res_model': 'formulario.prueba.ga',
                'view_mode': 'form',
                # 'view_type': 'form',
                'target': 'new',  # Abre en un modal (pop-up)
                'context': {
                    'default_planilla_id': self.planilla_id.id,  # Pasa el ID de planilla.recepcion al contexto
                },
            }
    

class LimpiezaExtremos(models.Model):
    _name = 'formulario.prueba.le'
    _description = 'LE: Limpieza Extremos'

    name = fields.Char(string='Nombre', related='planilla_id.descripcion', store=True)
    planilla_id = fields.Many2one('planilla.recepcion', string='Planilla Recepcion', ondelete='cascade')
    todos = fields.Boolean(string='Todos')
    aprobado = fields.Boolean(string='Aprobado', default=False)

    def aprobar_y_siguiente(self):
        # Alternar el estado del campo aprobado
        self.aprobado = True
        
        # Buscar un registro en 'formulario.prueba.iv' con el mismo 'planilla_id'
        iv_record = self.env['formulario.prueba.iv'].search([
            ('planilla_id', '=', self.planilla_id.id)
        ], limit=1)

        if iv_record:
            # Si existe un registro, abrir el formulario de ese registro
            return {
                'type': 'ir.actions.act_window',
                'name': 'IV: Inspección Visual',
                'res_model': 'formulario.prueba.iv',
                'view_mode': 'form',
                # 'view_type': 'form',
                'res_id': iv_record.id,
                'target': 'new',  # Abre en la misma ventana
            }
        else:
            # Si no existe un registro, crear uno nuevo y abrir el formulario
            return {
                'type': 'ir.actions.act_window',
                'name': 'IV: Inspección Visual',
                'res_model': 'formulario.prueba.iv',
                'view_mode': 'form',
                # 'view_type': 'form',
                'target': 'new',  # Abre en un modal (pop-up)
                'context': {
                    'default_planilla_id': self.planilla_id.id,  # Pasa el ID de planilla.recepcion al contexto
                },
            }

class InspeccionCalibres(models.Model):
    _name = 'formulario.prueba.ga'
    _description = 'GA: Inspección con Calibres'

    name = fields.Char(string='Nombre', related='planilla_id.descripcion', store=True)
    estado_general = fields.Boolean(string='Estado General', default=False)
    planilla_id = fields.Many2one('planilla.recepcion', string='Planilla Recepcion', ondelete='cascade')
    aprobado = fields.Boolean(string='Aprobado', default=False)

    def aprobar_y_siguiente(self):
        # Alternar el estado del campo aprobado
        self.aprobado = True
        
        # Buscar un registro en 'formulario.prueba.iv' con el mismo 'planilla_id'
        iv_record = self.env['formulario.prueba.me'].search([
            ('planilla_id', '=', self.planilla_id.id)
        ], limit=1)

        if iv_record:
            # Si existe un registro, abrir el formulario de ese registro
            return {
                'type': 'ir.actions.act_window',
                'name': 'IV: Inspección Visual',
                'res_model': 'formulario.prueba.me',
                'view_mode': 'form',
                # 'view_type': 'form',
                'res_id': iv_record.id,
                'target': 'new',  # Abre en la misma ventana
            }
        else:
            # Si no existe un registro, crear uno nuevo y abrir el formulario
            return {
                'type': 'ir.actions.act_window',
                'name': 'IV: Inspección Visual',
                'res_model': 'formulario.prueba.me',
                'view_mode': 'form',
                # 'view_type': 'form',
                'target': 'new',  # Abre en un modal (pop-up)
                'context': {
                    'default_planilla_id': self.planilla_id.id,  # Pasa el ID de planilla.recepcion al contexto
                },
            }
        

class MedicionEspesores(models.Model):
    _name = 'formulario.prueba.me'
    _description = 'ME: Medición de Espesores'

    name = fields.Char(string='Nombre', related='planilla_id.descripcion', store=True)
    # valor_medido_punto_a = fields.Boolean(string='Valor Medido[mm]', default=False)
    # valor_medido_punto_b = fields.Boolean(string='Estado de los Sellos', default=False)
    observaciones = fields.Text(string='Observaciones')
    planilla_id = fields.Many2one('planilla.recepcion', string='Planilla Recepcion', ondelete='cascade')
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado')
    ], string='Estado', default='borrador')

    # Valores traídos desde otro modelo como campos computados
    punto_a_minimo_admisible = fields.Char(string='Punto A - Minimo Adminisble[mm]')
    punto_b_minimo_admisible = fields.Char(string='Punto A - Valor Medido[mm]')
 
    # Campos para completar en el formulario
    punto_a_valor_medido = fields.Char(string='Punto B - Minimo Adminisble[mm]')
    punto_b_valor_medido = fields.Char(string='Punto B - Valor Medido[mm]')

    def rechazar(self):
        self.aprobado = 'rechazado'
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def aprobar_y_siguiente(self):
        self.estado = 'aprobado'
        
        # Buscar un registro en 'formulario.prueba.iv' con el mismo 'planilla_id'
        iv_record = self.env['formulario.prueba.pm'].search([
            ('planilla_id', '=', self.planilla_id.id)
        ], limit=1)

        if iv_record:
            # Si existe un registro, abrir el formulario de ese registro
            return {
                'type': 'ir.actions.act_window',
                'name': 'IV: Inspección Visual',
                'res_model': 'formulario.prueba.pm',
                'view_mode': 'form',
                # 'view_type': 'form',
                'res_id': iv_record.id,
                'target': 'new',  # Abre en la misma ventana
            }
        else:
            # Si no existe un registro, crear uno nuevo y abrir el formulario
            return {
                'type': 'ir.actions.act_window',
                'name': 'IV: Inspección Visual',
                'res_model': 'formulario.prueba.pm',
                'view_mode': 'form',
                # 'view_type': 'form',
                'target': 'new',  # Abre en un modal (pop-up)
                'context': {
                    'default_planilla_id': self.planilla_id.id,  # Pasa el ID de planilla.recepcion al contexto
                },
            }
        

class ParticulasMagnetizables(models.Model):
    _name = 'formulario.prueba.pm'
    _description = 'PM: Partículas Magnetizables'

    name = fields.Char(string='Nombre', related='planilla_id.descripcion', store=True)
    
    planilla_id = fields.Many2one('planilla.recepcion', string='Planilla Recepcion', ondelete='cascade')
    aprobado = fields.Boolean(string='Aprobado', default=False)

    def aprobar_y_siguiente(self):
        # Alternar el estado del campo aprobado
        self.aprobado = True
        
        # Buscar un registro en 'formulario.prueba.iv' con el mismo 'planilla_id'
        iv_record = self.env['formulario.prueba.lp'].search([
            ('planilla_id', '=', self.planilla_id.id)
        ], limit=1)

        if iv_record:
            # Si existe un registro, abrir el formulario de ese registro
            return {
                'type': 'ir.actions.act_window',
                'name': 'IV: Inspección Visual',
                'res_model': 'formulario.prueba.lp',
                'view_mode': 'form',
                # 'view_type': 'form',
                'res_id': iv_record.id,
                'target': 'new',  # Abre en la misma ventana
            }
        else:
            # Si no existe un registro, crear uno nuevo y abrir el formulario
            return {
                'type': 'ir.actions.act_window',
                'name': 'IV: Inspección Visual',
                'res_model': 'formulario.prueba.lp',
                'view_mode': 'form',
                # 'view_type': 'form',
                'target': 'new',  # Abre en un modal (pop-up)
                'context': {
                    'default_planilla_id': self.planilla_id.id,  # Pasa el ID de planilla.recepcion al contexto
                },
            }


class LiquidosPenetrantes(models.Model):
    _name = 'formulario.prueba.lp'
    _description = 'LP: Líquidos Penetrantes'

    name = fields.Char(string='Nombre')

class PruebaHidrostatica(models.Model):
    _name = 'formulario.prueba.ph'
    _description = 'PH: Prueba Hidrostática'

    name = fields.Char(string='Nombre')

class InformeFinal(models.Model):
    _name = 'formulario.prueba.inf'
    _description = 'INF: Informe Final'

    name = fields.Char(string='Nombre')


class ProjectTask(models.Model):
    _inherit = 'project.task'

    ingresos_ids = fields.Many2many('ingreso', string='Ingresos de Piezas')

    def action_create_ingreso(self):
        # Crear un nuevo registro en el modelo 'ingreso'
        new_ingreso = self.env['ingreso'].create({
            # Aquí puedes agregar cualquier valor predeterminado que necesites
            'cliente': self.partner_id.id,
            'numero_ot': self.id,
            'fecha': self.date_deadline,
            'responsable': [(6, 0, self.user_ids.ids)],
        })

        # Agregar el nuevo ingreso a la relación Many2many en la tarea actual
        self.ingresos_ids |= new_ingreso

        # Retornar una acción para abrir el formulario del nuevo ingreso
        return {
            'type': 'ir.actions.act_window',
            'name': 'Ingreso',
            'res_model': 'ingreso',
            'view_mode': 'form',
            'res_id': new_ingreso.id,
            'target': 'current',
        }
    
    def action_link_to_ingreso(self):
        self.ensure_one()
        
        if self.ingresos_ids:
            if len(self.ingresos_ids) == 1:
                # Abrir la vista del primer ingreso relacionado
                return {
                    'name': 'Ingreso',
                    'view_mode': 'form',
                    'res_model': 'ingreso',
                    'type': 'ir.actions.act_window',
                    'res_id': self.ingresos_ids[0].id,
                    'view_id': False,
                    'target': 'current',
                }
            else:
                # Filtrar y abrir la vista de árbol de ingresos relacionados
                return {
                    'name': 'Ingresos Relacionados',
                    'view_mode': 'tree,form',
                    'res_model': 'ingreso',
                    'type': 'ir.actions.act_window',
                    'domain': [('id', 'in', self.ingresos_ids.ids)],
                    'view_id': False,
                    'target': 'current',
                }
        else:
            # Manejar el caso donde no hay ingresos relacionados
            raise UserError('No se encontraron ingresos relacionados.')
    