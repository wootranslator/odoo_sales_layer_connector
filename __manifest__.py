{
    'name': 'Sales Layer PIM Connector',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales Layer PIM',
    'summary': 'Connector to Sales Layer PIM using API v2.0 (OData rest)',
    'author': 'Antigravity Developer',
    'depends': ['product', 'stock', 'mail', 'base_setup'],
    'data': [
        'security/ir.model.access.csv',
        # 'views/res_config_settings_views.xml',
        # 'views/product_template_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
