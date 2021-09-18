# -*- coding: utf-8 -*-
{
    'name': "DSC Custom Sales",

    'summary': """
        DSC Custom Sales""",

    'description': """
        This application add custom application to 
    """,

    'author': "Vetter Systems Inc",
    'website': "https://vettersystems.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'sequence': -102,

    # any module necessary for this one to work correctly
    'depends': ['base','sale','mail','account','website'],

    # always loaded
    'data': [        
        'views/stormsale.xml',       
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
