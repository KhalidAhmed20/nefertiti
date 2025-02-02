from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    orders_manager = fields.Char('مسؤول الطلبات')
