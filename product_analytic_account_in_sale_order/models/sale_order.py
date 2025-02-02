from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def product_analytic_account(self):
        for rec in self:
            rec.analytic_account_id = rec.product_id.analytic_account_id.id


