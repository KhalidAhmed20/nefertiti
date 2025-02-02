# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError



class purchase_order_inh(models.Model):
    _inherit = 'purchase.order'


    type = fields.Boolean(string="Import", default=False, translate=True)
    state = fields.Selection(selection_add=[('shipped', 'Shipped')])


    def get_shipped(self):
        for rec in self:
            if rec.state in ['purchase', 'done']:
                rec.state = 'shipped'
            else:
                raise UserError(_('Must be after confirm order'))


class sale_order_inh(models.Model):
    _inherit = 'sale.order'


    type = fields.Boolean(string="Import", default=False, translate=True)
    state = fields.Selection(selection_add=[('shipped', 'Shipped')])


    def get_shipped(self):
        for rec in self:
            if rec.state in ['sale', 'done']:
                rec.state = 'shipped'
            else:
                raise UserError(_('Must be after confirm order'))





