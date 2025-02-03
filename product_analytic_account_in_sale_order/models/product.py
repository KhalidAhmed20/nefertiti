from odoo import api, fields, models


class Product(models.Model):
    _inherit = 'product.template'

    analytic_account_id = fields.Many2one('account.analytic.account', "Analytic Account")
