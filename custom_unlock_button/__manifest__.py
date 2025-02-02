{
    'name': 'Custom Unlock Button',
    'version': '1.0',
    'summary': 'Add Lock/Unlock buttons with group restrictions in stock picking form',
    'author': 'Khalid',
    'depends': ['stock'],
    'data': [
        'security/custom_lock_unlock_button_security.xml',
        # 'security/ir.model.access.csv',
        # 'views/hide_stock_quant_price_groups.xml',
        'views/custom_lock_unlock_button_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
