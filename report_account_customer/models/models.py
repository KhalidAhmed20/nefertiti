# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ImportantJournalLedger(models.TransientModel):
    _name = 'general.ledger.vendor.wizard'
    _description = 'general ledger vendor wizard'

    name = fields.Char()
    date_from = fields.Date(string="Date From", required=True, )
    date_to = fields.Date(string="Date To", required=True, )
    partner_ids = fields.Many2many('res.partner', string='customer')

    def export_product(self):
        for rec in self:
            for id_partner in rec.partner_ids:
                account_move_lines = self.env['account.move.line'].search([
                    ('date', '>=', self.date_from),
                    ('date', '<=', self.date_to),
                    ('partner_id', '=', id_partner.id),
                    ('move_id.state', '=', 'posted'),
                    ('account_id.user_type_id', 'in', [self.env.ref('account.data_account_type_receivable').id,
                                                       self.env.ref('account.data_account_type_payable').id]),
                ])
                if not account_move_lines:
                    raise ValidationError(
                        f"No invoices found for the selected customer ({id_partner.name}) within the date.")

            if not rec.partner_ids:
                rec.partner_ids = self.env['res.partner'].sudo().search([('customer_rank', '>', 0)]).ids
            return self.env.ref('report_account_customer.report_action_id_general_ledger_customer').report_action(self)
