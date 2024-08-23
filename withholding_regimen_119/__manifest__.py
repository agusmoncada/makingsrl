# -*- coding: utf-8 -*-
{
    "name": "Withholding regimen 119",
    'version': '17.0.1.0.0',
    'category': 'Localization/Argentina',
    'author': 'IngenioSolutions',
    'website': 'https://ingeniosolutions.com.ar/',
    'license': 'AGPL-3',
    'summary': '',
    "depends": [
        "l10n_ar_account_withholding",
    ],
    "data": [
        'views/afip_tabla_ganancias_escala_view.xml',
        'data/tabla_ganancias_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
