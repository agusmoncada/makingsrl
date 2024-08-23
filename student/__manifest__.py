# informes/__manifest__.py

{
    'name': 'Informes',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Módulo de Informes Personalizados',
    'description': 'Este módulo proporciona informes personalizados.',
    'author': 'Tu Nombre',
    'website': 'https://www.tusitio.com',
    'depends': ['base','project'],
    'data': [
        'security/ir.model.access.csv',
        'views/student_view.xml',
    ],
    'installable': True,
    'application': True,
}
