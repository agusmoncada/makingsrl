# -*- coding: utf-8 -*-

{
    'name': 'FIX Customer Follow Up Management',
    'version': '17.0.1.0.0',
    'category': 'Accounting',
    'description': """FIX Customer FollowUp Management""",
    'summary': """FIX Customer FollowUp Management""",
    'author': 'IngenioSolutions',
    'license': 'LGPL-3',
    'website': 'https://ingeniosolutions.com.ar/',
    'depends': [
        'om_account_followup',
    ],
    'data': [
        'data/data.xml',
        'views/report_followup.xml',
    ],
}
