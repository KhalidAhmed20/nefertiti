# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'custom_confirm_record',
    'version': '0.1',
    'category': 'odoo',
    'author': 'ibs',
    'sequence': -600,
    'summary': 'custom_confirm_record',
    'description': """custom_confirm_record'""",
    'depends': ['base','sale','stock'],
    'data': [
        'views/confirm_records.xml'


    ],
    'demo': [],
    'installable': True,
    'applocation': True,
    'auto_install': False,
    'license': 'LGPL-3',

}
