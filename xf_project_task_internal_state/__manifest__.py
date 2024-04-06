# -*- coding: utf-8 -*-
{
    'name': 'Internal State for Tasks',
    'version': '1.1.0',
    'summary': '''
    The module introduces internal states (new, open, suspended, done) 
    for tasks and task stages to facilitate 
    the easy determination of task statuses.
    ''',
    'category': 'Project',
    'author': 'XFanis',
    'support': 'xfanis.dev@gmail.com',
    'website': 'https://xfanis.dev/odoo.html',
    'license': 'OPL-1',
    'price': 5,
    'currency': 'EUR',
    'description':
        """
        The module introduces internal states (new, open, suspended, done) 
        for tasks and task stages to facilitate the easy determination of task statuses.
        """,
    'data': [
        # Views
        'views/project_task.xml',
        'views/project_task_type.xml',
    ],
    'demo': [
        'data/demo/project_task_type.xml',
    ],
    'depends': ['project'],
    'assets': {},
    'images': [
        'static/description/xf_project_task_internal_state.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
