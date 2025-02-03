# -*- coding: utf-8 -*-

from odoo import models, fields, api


class purchaseorderinh(models.Model):
    _inherit = 'purchase.order'

    langu = fields.Selection(related="partner_id.lang", readonly=False)



class saleorderinh(models.Model):
    _inherit = 'sale.order'

    langu = fields.Selection(related="partner_id.lang", readonly=False)


class stockpickinginh(models.Model):
    _inherit = 'stock.picking'

    langu = fields.Selection(related="partner_id.lang", readonly=False)


