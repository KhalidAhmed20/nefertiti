# -*- coding: utf-8 -*-

from odoo import fields, models

class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'

    categ_id = fields.Many2one(
        related='product_id.categ_id',
        string='Product Category',
        store=True,
        readonly=True
    )
    location_id = fields.Many2one(
        related='stock_move_id.location_id',
        string='Location',
        store=True,
        readonly=True
    )
    date = fields.Date(string='Date')

