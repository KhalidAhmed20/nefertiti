from odoo import api, fields, models


class AccountAccountant(models.Model):
    _inherit = 'account.account'

    show_cost_of_goods_sold = fields.Boolean(string="Hide Cost Of Goods Sold")

