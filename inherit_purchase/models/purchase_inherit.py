from odoo import models, fields, api, _


class SalesOrderInherit(models.Model):
    _inherit = 'purchase.order'

    exchange_coefficient = fields.Char(string=' معامل الصرف')

