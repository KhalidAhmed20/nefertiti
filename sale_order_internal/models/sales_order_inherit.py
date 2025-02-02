from odoo import models, fields, api, _


class SalesOrderInherit(models.Model):
    _inherit = 'sale.order'

    reference_number = fields.Char(string=' رقم اشارة العميل')

    def action_create_batch_invoice(self):
        for rec in self:
            rec._create_invoices()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'name': _('Customer Invoices'),
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.invoice_ids.ids)],
        }
