# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InventoryLocationWizard(models.TransientModel):
    _name = 'inventory.location.wizard'
    _description = 'general ledger vendor wizard'

    name = fields.Char()
    date_from = fields.Date(string="Date From", required=True, )
    date_to = fields.Date(string="Date To", required=True, )
    stock_id = fields.Many2one('stock.warehouse', 'Warehouse', required=True, )
    location_ids = fields.Many2many(comodel_name="stock.location", string="Locations")

    def export_product(self):
        for rec in self:
            if not rec.location_ids:
                rec.location_ids = self.env['stock.location'].sudo().search([]).ids
            return self.env.ref('report_inventory_location.report_action_id_inventory_location').report_action(self)
