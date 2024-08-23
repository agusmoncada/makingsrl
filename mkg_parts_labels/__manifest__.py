# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': "MKG Parts Labels",
    'summary': """
        Module that adds Making part labels in part creation 
        in the Reports module. Also add an ABM in Reports/Settings 
        for its administration.
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
                'student',
                ],

    'data': [
        'security/ir.model.access.csv',
        'views/mkg_parts_labels_views.xml',
        'views/ingresos_views.xml',
        # 'data/data.xml',
    ],
}
