from odoo import api, fields, models, _


class StockPiking(models.Model):
    _inherit = 'stock.picking'

    def action_server_validate(self):
        for pick in self:
            if pick.picking_type_id.code == 'incoming':
                for line in pick.move_ids_without_package:
                    line.quantity_done = line.product_uom_qty
                context = {'skip_sanity_check': True}
                pick.with_context(**context).button_validate()
