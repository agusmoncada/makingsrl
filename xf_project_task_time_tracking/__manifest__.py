# -*- coding: utf-8 -*-
{
    'name': 'Task Time Tracking',
    'version': '1.0.0',
    'summary': '''
    Simplify project time tracking. 
    Our time tracking software automatically records task progress and time spent. 
    No need to manually pause for breaks or weekends. 
    Stay efficient with accurate time entries, even when tasks change hands or stages. 
    Easy time management for your projects.
    | automated time tracking
    | task progress recording
    | project task tracker
    | project task tracking
    | project task timer
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
        Task Time Tracking App.
        Simplify project time tracking. 
        Our module automatically records task progress and time spent, ensuring accuracy without manual effort. 
        No need to pause for breaks or weekends – the system handles non-working hours seamlessly. 
        Stay efficient with accurate time entries, even when tasks change hands or stages. 
        Easy time management for your projects, keeping you in control and your team on track.
        """,
    'data': [
        # Access
        # 'security/security.xml',
        'security/ir.model.access.csv',
        # Views
        'views/project_project.xml',
        'views/project_task.xml',
        # Data
        'data/ir_cron_data.xml',
    ],
    'depends': [
        'project',
        'xf_project_task_internal_state',
        'xf_project_task_allocation_percent',
    ],
    'assets': {},
    'images': [
        'static/description/xf_project_task_time_tracking.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# Todo
# Track Time by separate button
# Converting to hr timesheet
