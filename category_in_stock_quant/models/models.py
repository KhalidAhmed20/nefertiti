# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    categ_id = fields.Many2one(comodel_name="product.category", string="Category", required=False,related='product_id.categ_id',store=True )
    cost_cost = fields.Float(string="Cost",  required=False,compute='get_cost_cost',store=True )




    @api.depends('quantity','value')
    def get_cost_cost(self):
        print('sssssssssssssssssssssssssssssssssssssssssss')
        for rec in self:
            print('sssssssssssssssssssssssssssssssssssssssssss')
            if rec.value > 0:
                print('dddddddddddddddddddddddddddddddddddddddddd')
                rec.cost_cost=rec.value / rec.quantity
            else:
                print('qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
                rec.cost_cost=0



