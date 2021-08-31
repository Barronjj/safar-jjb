# -*- coding: utf-8 -*-pack
{
    'name': 'GLS France Shipping Integration',
    'category': 'Website',
    'author': "Vraja Technologies",
    'version': '13.25.06.21',
    'summary': """We are providing following modules, Shipping Operations, shipping, odoo shipping integration,odoo shipping connector, dhl express, fedex, ups, gls, usps, stamps.com, shipstation, bigcommerce, easyship, amazon shipping, sendclound, ebay, shopify.""",
    'description': """""",
    'depends': ['delivery'],
    'data': ['views/res_company.xml',
             'views/stock_picking.xml',
             'views/delivery_carrier.xml'
             ],
    'images': ['static/description/GLS_Cover_Image.png'],
    'maintainer': 'Vraja Technologies',
    'website': 'www.vrajatechnologies.com',
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'live_test_url': 'http://www.vrajatechnologies.com/contactus',
    'price': '279',
    'currency': 'EUR',
    'license': 'OPL-1',
}

# version changelog
# 13.25.06.21 add service option in delivery carrier
