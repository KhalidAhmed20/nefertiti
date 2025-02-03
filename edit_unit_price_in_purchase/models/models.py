# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrderLineInherit(models.Model):
    _inherit = 'purchase.order.line'

    def _onchange_quantity(self):
        res = super(PurchaseOrderLineInherit, self)._onchange_quantity()
        for rec in self:
            rec.price_unit = 0
        return res
