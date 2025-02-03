from odoo import models, fields, api, _


class MrpProductionRequest(models.Model):
    _inherit = 'mrp.production.request'

    customer = fields.Char(string='Customer')
    request_official = fields.Char(string='مسئول الطلب')


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    product = fields.Char(string='المنتج')
    quantity = fields.Char(string='الكمية')
    size = fields.Char(string='المقاس')
    grams = fields.Char(string='الجرام')
    toppings = fields.Char(string='الطبقة')
    color = fields.Char(string='اللون')