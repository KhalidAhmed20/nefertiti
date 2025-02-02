# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NewModule(models.Model):
    _inherit = 'stock.move.line'

    analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account")


class EditStockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(EditStockPicking, self).button_validate()
        for rec in self:
            for lines in rec.move_line_ids_without_package:
                moves = self.env['account.move.line'].search([])
                for move in moves:
                    if move.name:
                        if rec.name in move.name and move.product_id == lines.product_id:
                            # if move.account_id.user_type_id.id in [
                            #     self.env.ref('account.data_account_type_direct_costs').id,
                            #     self.env.ref('account.data_account_type_expenses').id]:
                            move.analytic_account_id = lines.analytic_account_id
        return res
