# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': "MKG We Send",
    'summary': """
        Module to support referrals within the projects module. 
        Includes an ABM for administration, and possibility of 
        creation from Tasks view.
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
        'views/mkg_we_send_views.xml',
        'views/project_task_form.xml',
        'data/data.xml',
    ],
}
