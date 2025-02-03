from odoo import models, fields, api, _


class SalesOrderInherit(models.Model):
    _inherit = 'account.payment'

    exchange_coefficient_customer = fields.Char(string=' معامل الصرف')

