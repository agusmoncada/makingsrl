{
    'name': 'Reporte de Retenciones Ganancias en Excel',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Genera un reporte en Excel de las retenciones de ganancias',
    'description': """
Este módulo permite exportar un reporte en formato Excel que incluye las retenciones de ganancias con los campos especificados.
    """,
    'author': 'Irene Colichelli',
    'website': 'https://www.tuweb.com',
    'depends': ['base', 'account', 'report_xlsx', 'l10n_ar'],
    'data': [
        'wizard/wizard.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
