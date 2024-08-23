# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': "Journal in Report Payment Receipts",
    'summary': """
        Add Journal field to report Payment Receipts
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
                'account',
                ],

    'data': [
        'views/report_payment_receipt.xml',
    ],
}
