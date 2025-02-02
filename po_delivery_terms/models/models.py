# -*- coding: utf-8 -*-

from unicodedata import name
from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    delivery_terms_id = fields.Many2one('delivery.terms', string='Delivery Terms', required=True)


class DeliveryTerms(models.Model):   
    _name = 'delivery.terms'
    _rec_name='delivery_terms_name'

    delivery_terms_name = fields.Char('Name')