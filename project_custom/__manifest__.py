# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': "Project Custom",
    'summary': """
        Module that adds extra customizations required by Making in the project module
    """,
    'author': "SalusERP",
    "maintainers": ["franco0310"],
    "website": "https://www.saluserp.com/",
    "license": "AGPL-3",
    "category": "Project",
    "version": "17.0.0.0.0",
    "installable": True,
    "application": False,
    'depends': ['base',
                'project',
                ],

    'data': [
        #'security/ir.model.access.csv',
        'views/view_task_form.xml',
        'views/view_task_kanban.xml',
    ],
}
