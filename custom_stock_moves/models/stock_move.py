from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.move"

    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)
    product_category_id = fields.Many2one(
        'product.category',
        string="Category",
        related='product_id.categ_id',
        store=True
    )

    @api.depends('product_qty', 'price_unit')
    def _compute_total_price(self):
        for move in self:
            if move.product_qty and move.price_unit:
                move.total_price = move.product_qty * move.price_unit
            else:
                move.total_price = 0
