# -*- coding: utf-8 -*-
{
    'name': "DSC Custom Attendance",

    'summary': """
        DSC Custom Attendance""",

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
    'sequence': -105,

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [        
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/dschrattendance.xml',
        'views/dscworkshiftschedule.xml',
    ],
    'qweb': ['static/src/xml/qweb.xml'],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
