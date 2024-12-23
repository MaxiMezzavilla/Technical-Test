{
    'name': 'Gestión de Canales de Venta',
    'version': '1.0',
    'author': 'Maximiliano Mezzavilla',
    'category': 'Sales',
    'summary': 'Gestión de canales de venta con almacenes y diarios asociados.',
    'description': """
        Este módulo permite gestionar canales de venta, asignando almacenes para la entrega de productos y diarios de facturación. 
        Incluye seguimiento de cambios a través del chatter para auditoría.
    """,
    'depends': ['base', 'sale', 'stock','sale_stock', 'account', 'mail'],
    'data': [
        'data/channel_sequence.xml',
        'views/sales_channel_view.xml',
        'views/credit_group_view.xml',
        'views/sales_view.xml',
        'views/res_partner_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
