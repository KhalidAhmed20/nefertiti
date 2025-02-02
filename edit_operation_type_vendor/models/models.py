# -*- coding: utf-8 -*-

from odoo import models, fields, api

class EditResPartner(models.Model):
    _inherit = 'res.partner'

    picking_type_id = fields.Many2one('stock.picking.type', 'Picking Type',)




class EditPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.onchange('partner_id')
    def get_picking_type_id(self):
        for rec in self:
            rec.picking_type_id=rec.partner_id.picking_type_id.id
