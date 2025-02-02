# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InventoryInherit(models.Model):
    _inherit = 'stock.production.lot'

    size = fields.Char(string='المقاس')
    grams = fields.Char(string='الجرام')
    layer = fields.Char(string='الطبقة')


class InventoryInheritQuant(models.Model):
    _inherit = 'stock.quant'

    size = fields.Char(related='lot_id.size',string='المقاس')
    grams = fields.Char(related='lot_id.grams',string='الجرام')
    layer = fields.Char(related='lot_id.layer', string='الطبقة')

    @api.onchange('layer')
    def test_print(self):
        print(self.size)
