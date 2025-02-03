# -*- coding: utf-8 -*-
{
    'name': "reports_nefertity",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_holidays','adjustments','loans_and_addvance'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/report_lone.xml',
        'views/report_over_time.xml',
        'views/report_salary_advance.xml',
        'views/report_time_of.xml',
        'views/report_adjustments.xml',
        'views/report_rewards.xml',
        'views/report_penalities.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
