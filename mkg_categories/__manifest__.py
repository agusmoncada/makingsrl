# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': "MKG Categories",
    'summary': """
        Module that adds Making categories in the creation of tasks, 
        in the projects module. Also add an ABM in Project/Configuration 
        for administration.
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
        'security/ir.model.access.csv',
        'views/mkg_categories_views.xml',
        'views/project_task_form.xml',
        'data/data.xml',
    ],
}
