# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EditStockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.onchange('date_done')
    def change_date_account(self):
        for rec in self:
            moves = self.env['account.move'].search([('stock_move_id','!=',False)])
            for move in moves:
                if move.ref:
                    # print('rec.name',rec.name)
                    # print('move.ref',move.ref)
                    if rec.name in move.ref :
                        if rec.date_done:
                            print('move', move)
                            move.sudo().write({'date': rec.date_done.date()})
                # print('line.account_move_ids',line.account_move_ids)


            # move_stocks = self.env['stock.move'].sudo().search([('picking_id', '=', self.id)])
            # print('move_stocks', move_stocks)
            # for line in move_stocks:
            #     print('line', line)
            #     print('2222222222222')
            #     print('line.account_move_ids', line.account_move_ids)
            #     for account in line.account_move_ids:
            #         print('account', account)
            #         print('account.date', account.date)
            #         print('3333333333')
            #         account.sudo().write({'date': rec.date_done.date()})
            #         # account.date=rec.date_done.date()
            #         print('account.date', account.date)
            #         print('rec.date_done.date()', rec.date_done.date())


class EditStockMove(models.Model):
    _inherit = 'stock.move'

    date = fields.Datetime(
        'Date', default=fields.Datetime.now, index=True, required=False,
        states={'done': [('readonly', True)]}, related='picking_id.date_done' , store=True ,
        help="Move date: scheduled date until move is done, then date of actual move processing")


class EditStockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    date = fields.Datetime('Date', required=False, related='picking_id.date_done',store=True)



class EditPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    date_approve = fields.Datetime('Confirmation Date', readonly=0, index=True, copy=False)


class EditSaleOrder(models.Model):
    _inherit = 'sale.order'

    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True,
                                 states={'sale': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False,
                                 default=fields.Datetime.now,
                                 help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")
