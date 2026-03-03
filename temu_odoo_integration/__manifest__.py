{
    'name': 'Temu Odoo Integration',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Import sales orders from Temu to Odoo 18',
    'description': """
        This module allows importing sales orders from Temu marketplace.
        Includes SKU mapping, fiscal position mapping, payment mapping, and tracking synchronization.
    """,
    'author': 'Antigravity',
    'depends': ['sale_management', 'stock', 'delivery'],
    'data': [
        'security/ir.model.access.csv',
        'data/temu_data.xml',
        'views/temu_connector_view.xml',
        'wizard/temu_order_import_view.xml',
        'wizard/temu_dummy_wizard_view.xml',
    ],
    'installable': True,
    'application': True,
    'post_init_hook': 'post_init_hook',
    'license': 'LGPL-3',
}
