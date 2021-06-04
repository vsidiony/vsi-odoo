# -*- coding: utf-8 -*-
{
    'name': "DSC Storm",

    'summary': """
        DSC Storm Application""",

    'description': """
        This ia a storm application
    """,

    'author': "Vetter Systems Inc",
    'website': "https://vettersystems.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'sequence': -100,

    # any module necessary for this one to work correctly
    'depends': ['base','sale','mail','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/sequenceinvoice.xml',
        'views/stormlog.xml',
        'views/stormsale.xml',
        'views/accountmove.xml',
        #'views/views.xml',
        'views/templates.xml',
        
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    'installable': True,
    'application': True,
    'auto_install': True,
}
