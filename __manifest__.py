{
    'name': 'Sales Layer PIM Connector',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Sincronización de variantes con Sales Layer PIM',
    'author': 'Tu Nombre/Empresa',
    'depends': ['product', 'stock', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
