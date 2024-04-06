# -*- coding: utf-8 -*-
{
    'name': 'Project Task Allocation Percent',
    'version': '1.0.0',
    'summary': """
    The module helps to control resource allocation percentage.
    Each user can set Assignment Units for task from 0 to 100 and the system will control Percent Allocation per Employee.
    User will not be able to start many parallel tasks.
    | Assignment Units
    | Total percent allocation
    | Parallel task restriction
    | Restrict parallel tasks
    | Percent Allocation
    | User Workload
    | Employee Workload
    """,
    'category': 'Project',
    'author': 'XFanis',
    'support': 'xfanis.dev@gmail.com',
    'website': 'https://xfanis.dev/odoo.html',
    'license': 'OPL-1',
    'price': 5,
    'currency': 'EUR',
    'description':
        """
        The module helps to control resource allocation percentage.
        Each user can set Assignment Units for task from 0 to 100 and the system will control Percent Allocation per Employee.
        User will not be able to start many parallel tasks.
        """,
    'data': [
        'views/project_task.xml',
        'views/project_task_type.xml',
    ],
    'depends': ['project'],
    'qweb': [],
    'images': [
        'static/description/xf_project_task_allocation_percent.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
