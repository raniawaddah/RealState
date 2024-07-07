# -*- coding: utf-8 -*-
{
    'name': "App One",


    'author': "Rania",


    'category': '',
    'version': '0.1',

    'depends': ['base', 'sale', 'mail'],

    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner.xml',
        'views/tag_view.xml',
        'views/sale_order_view.xml',
        'reports/property_report.xml',

    ],
    'assets': {
      'web.assets_backend':['app_one/static/src/css/property.css']
    },

    'application':True,

}
