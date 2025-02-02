# -*- coding: utf-8 -*-

from odoo import models, fields, api
from num2words import num2words


def convert_to_wordss(amount):
    integer_part, decimal_part = str(amount).split('.')
    words_integer = num2words(int(integer_part), lang='ar')
    words_decimal = ""
    if decimal_part:
        words_decimal = num2words(int(decimal_part), lang='ar')
        words_decimal = f" فاصلة {words_decimal} قرشا"

    result = f"{words_integer} جنيها{words_decimal}"
    return result


class ImportantJournalLedger(models.TransientModel):
    _inherit = 'general.ledger.vendor.wizard'

    def print_report(self):
        report = {}
        valss = {}
        partners = []
        for partner in self.partner_ids:
            data = []
            move_data = []
            partner_name = ""
            valss = {}
            move_name = ""
            move_ref = ""
            move_debit = ""
            move_credit = ""
            product_name = ""
            product_quantity = ""
            product_price_unit = ""
            product_price_subtotal = ""
            account_invoice_ref = ""
            show_cost_of_goods = False
            total_debitt = ""
            total_creditt = ""

            balancee = []
            date = ""
            initial_balance = 0
            balance = 0.0
            total_debit = 0.0
            total_credit = 0.0

            partner_name = str(partner.name)

            account_move_lines = self.env['account.move.line'].search([
                ('date', '>=', self.date_from),
                ('date', '<=', self.date_to),
                ('partner_id', '=', partner.id),
                ('move_id.state', '=', 'posted'),
                ('move_id.name', 'not like', 'STJ%'),
                ('account_id.show_cost_of_goods_sold', '=', False),
                ('account_id.user_type_id', 'in', [self.env.ref('account.data_account_type_receivable').id,
                                                   self.env.ref('account.data_account_type_payable').id]),
            ])
            account_move_lines_balance = self.env['account.move.line'].search([
                ('date', '<=', self.date_from),
                ('partner_id', '=', partner.id),
                ('move_id.state', '=', 'posted'),
                ('move_id.name', 'not like', 'STJ%'),
                ('account_id.show_cost_of_goods_sold', '=', False),
                ('account_id.user_type_id', 'in', [self.env.ref('account.data_account_type_receivable').id,
                                                   self.env.ref('account.data_account_type_payable').id]),
            ], order="date")
            print(account_move_lines)
            print(account_move_lines_balance)
            if account_move_lines_balance:
                for move_balance in account_move_lines_balance:
                    # initial_balance = initial_balance + move_balance.debit - move_balance.credit
                    balance = balance + move_balance.debit - move_balance.credit

            for move in account_move_lines:
                product_namee = ""
                product_quantityy = ""
                product_price_unitt = ""
                product_price_subtotall = ""
                account_invoice_reff = ""
                if True:

                    total_credit += move.credit
                    total_debit += move.debit
                    # balance = initial_balance + move.debit - move.credit
                    balance = balance + move.debit - move.credit
                    date = str(move.date)
                    move_name = str(move.move_id.name)
                    move_ref = str(move.ref)
                    move_debit = str(move.debit)
                    move_credit = str(move.credit)
                    # initial_balance = balance
                    balancee.append(balance)

                    account_invoice = self.env['account.move'].sudo().search(
                        [('id', '=', move.move_id.id), ('state', '=', 'posted'), ], limit=1)
                    if account_invoice:
                        if account_invoice.invoice_line_ids.product_id:
                            print('account_invoice.invoice_line_ids', account_invoice.invoice_line_ids)
                            # if 'INV' in move.move_id.name:
                            #     account_invoice=self.env['account.invoice'].sudo().search([('number','=',move.move_id.name)],limit=1)
                            #     account_invoice = self.env['account.invoice'].sudo().search([('move_id', '=', move.move_id.id)], limit=1)
                            # sheet.write(row, 1, "product", format2)
                            # sheet.set_column(row, 1, 40)
                            # sheet.write(row, 2, 'QTY', format2)
                            # sheet.write(row, 3, 'Price', format2)
                            # sheet.write(row, 4, 'Amount', format2)
                            # row += 1
                            for line in account_invoice.invoice_line_ids:
                                product_namee = str(line.product_id.name)
                                product_quantityy = str(line.quantity)
                                product_price_unitt = str(line.price_unit)
                                product_price_subtotall = str(line.price_subtotal)
                                account_invoice_reff = str(account_invoice.ref)

                            product_name = str(product_namee)
                            product_quantity = str(product_quantityy)
                            product_price_unit = str(product_price_unitt)
                            product_price_subtotal = str(product_price_subtotall)
                            account_invoice_ref = str(account_invoice_reff)
                            # row += 1
                        # elif 'INV' not in move.move_id.name:
                        elif move.payment_id:
                            # sheet.write(row, 3, "الرقم", format1)
                            # sheet.set_column(row, 3, 40)
                            # sheet.write(row, 4, 'التاريخ', format1)
                            # sheet.write(row, 5, 'المبلغ', format1)
                            # sheet.write(row, 6, 'البنك', format1)
                            # sheet.write(row, 5, 'Drawer Name', format1)

                            for check in move.payment_id.payment_check_lines:
                                product_namee = str(check.check_number)
                                product_quantityy = str(check.check_date)
                                product_price_unitt = str(check.check_amount)
                                product_price_subtotall = str(check.check_bank_id.name)
                                account_invoice_reff = str(check.communication)

                            product_name = str(product_namee)
                            product_quantity = str(product_quantityy)
                            product_price_unit = str(product_price_unitt)
                            product_price_subtotal = str(product_price_subtotall)
                            account_invoice_ref = str(account_invoice_reff)

                        total_debitt = str(total_debit)

                    valss = {

                        'product_name': product_name,
                        'product_quantity': product_quantity,
                        'product_price_unit': product_price_unit,
                        'product_price_subtotal': product_price_subtotal,
                        'account_invoice_ref': account_invoice_ref

                    }

                vals = {
                    'date': date,
                    'move_name': move_name,
                    'move_ref': move_ref,
                    'move_debit': move_debit,
                    'move_credit': move_credit,
                    'balance': balance,
                    'product_name': product_name,
                    'product_quantity': product_quantity,
                    'product_price_unit': product_price_unit,
                    'product_price_subtotal': product_price_subtotal,
                    'account_invoice_ref': account_invoice_ref,
                    'data': valss
                }
                move_data.append(vals)
            cre = convert_to_wordss(total_credit)
            deb = convert_to_wordss(total_debit)
            bal = convert_to_wordss(balance)
            par = {
                'partner_name': partner_name,
                'move_data': move_data,
                'total_debit': total_debit,
                'total_credit': total_credit,
                'balance': balance,
                # 'initial_balance': initial_balance,
                'total_debit_words': deb,
                'total_credit_words': cre,
                'balance_words': bal

            }
            partners.append(par)

        report['partners'] = partners
        report['start_date'] = self.date_from
        report['end_date'] = self.date_to

        print(report)
        return self.env.ref('edit_general_ledger_customer.id_general_ledger_vendor_pdf').report_action(self,
                                                                                                       data=report)
