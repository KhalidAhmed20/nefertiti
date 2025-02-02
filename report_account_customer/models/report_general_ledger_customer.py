# -*- coding: utf-8 -*-


from odoo import _, api, fields, models
from io import BytesIO
import base64
from num2words import num2words


#
# def convert_to_words(amount):
#     integer_part, decimal_part = str(amount).split('.')
#     words_integer = num2words(int(integer_part), lang='ar')
#     words_decimal = ""
#     if decimal_part:
#         words_decimal = num2words(str(decimal_part), lang='ar')
#         words_decimal = f" فاصلة {words_decimal} قرشا"
#
#     result = f"{words_integer} جنيها{words_decimal}"
#     return result


class GeneralLedgerAccount(models.AbstractModel):
    _name = 'report.report_account_customer.report_customer'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'GeneralLedgerAccount'

    import base64

    def generate_xlsx_report(self, workbook, data, partners):
        global opening_debit
        sheet = workbook.add_worksheet('General Ledger Report')
        sheet.set_paper(9)
        sheet.right_to_left()
        company = self.env.user.company_id
        company_name = company.name
        sheet.set_row(0, 80)
        sheet.set_column('J:J', 100)
        sheet.set_column('K:K', 120)
        cell_format = workbook.add_format({'align': 'center', 'font_size': 15})
        sheet.merge_range('C3:D3', company_name, cell_format)
        # sheet.write('F2', company_name, cell_format)
        format1 = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'valign': 'vcenter', 'bold': True, 'bg_color': '#D5D5D5',
             'color': 'black',
             'border': 2})
        for row in range(8, 37):
            for col in range(0, 9):
                sheet.write(row, col, '', format1)
        if company.logo:
            image_data = BytesIO(base64.b64decode(company.logo))
            sheet.insert_image('C1:D1', 'logo.png', {'image_data': image_data, 'x_scale': 0.3, 'y_scale': 0.18})
            # sheet.merge_range('F1:G1', 'logo.png', {'image_data': image_data, 'x_scale': 0.005, 'y_scale': 0.005})
        # Rest of your code...
        for obj in partners:

            report_name = obj.name
            # One sheet by partner

            format0 = workbook.add_format({'font_size': 12, 'align': 'center'})
            format1 = workbook.add_format(
                {'font_size': 12, 'align': 'center', 'valign': 'vcenter', 'bold': True, 'bg_color': '#D5D5D5',
                 'color': 'black',
                 'border': 2})
            format2 = workbook.add_format(
                {'font_size': 12, 'align': 'center', 'bold': True,
                 'border': 1})
            format4 = workbook.add_format(
                {'font_size': 10, 'align': 'center', 'bold': True,
                 'border': 1})
            format10 = workbook.add_format(
                {'align': 'center', 'bold': True, 'bg_color': '#FF6600', 'border': 5, 'font_size': 12})
            format3 = workbook.add_format(
                {'align': 'center', 'bold': True, 'bg_color': '#FFFFFF', 'color': 'black', 'border': 5,
                 'font_size': 12})
            merge_format = workbook.add_format({
                'border': 1,
                'align': 'center',
                'valign': 'vcenter'
            })
            row = 4
            if obj.partner_ids:
                for partner in obj.partner_ids:
                    initial_balance = 0
                    balance = 0
                    total_debit = 0
                    total_credit = 0
                    deb = ''
                    cre = ''
                    bal = ''
                    sheet.merge_range(row, 1, row, 5, partner.name, format3)
                    row += 1
                    sheet.write(row, 1, 'من : ' + str(obj.date_from), format0)
                    sheet.write(row, 4, 'الي : ' + str(obj.date_to), format0)
                    row += 1
                    sheet.write(row, 0, 'التاريخ', format3)
                    sheet.set_column(row, 0, 28)
                    sheet.set_row(row, 17)
                    sheet.write(row, 1, 'الحركة', format3)
                    sheet.write(row, 2, 'الاصناف', format3)
                    sheet.write(row, 3, 'الكمية', format3)
                    # sheet.write(row, 4, 'السعر', format3)
                    sheet.write(row, 4, 'السعر', format3)
                    sheet.write(row, 5, 'المرجع (رقم الاشارة)', format3)
                    # sheet.write(row, 7, 'مدين', format3)
                    sheet.write(row, 6, 'المدين', format3)
                    sheet.write(row, 7, 'دائن', format3)
                    sheet.write(row, 8, 'الرصيد', format3)
                    sheet.set_column(row, 6, 4)
                    account_move_lines = self.env['account.move.line'].search([
                        ('date', '>=', obj.date_from),
                        ('date', '<=', obj.date_to),
                        ('partner_id', '=', partner.id),
                        ('move_id.state', '=', 'posted'),
                        ('account_id.user_type_id', 'in', [self.env.ref('account.data_account_type_receivable').id,
                                                           self.env.ref('account.data_account_type_payable').id]),
                    ], order="create_date")
                    account_move_lines_balance = self.env['account.move.line'].search([
                        ('date', '<', obj.date_from),
                        ('partner_id', '=', partner.id),
                        ('move_id.state', '=', 'posted'),
                        ('account_id.user_type_id', 'in', [self.env.ref('account.data_account_type_receivable').id,
                                                           self.env.ref('account.data_account_type_payable').id]),
                    ], order="create_date")
                    for move_balance in account_move_lines_balance:
                        initial_balance = initial_balance + move_balance.debit - move_balance.credit
                    row += 1
                    sheet.write(row, 5, "الرصيد الافتتاحي", format2)
                    # sheet.write(row+1, 6, initial_balance, format2)
                    account_invoice = self.env['account.move'].sudo().search(
                        [('id', '=', account_move_lines[0].move_id.id), ('state', '=', 'posted'), ], limit=1)
                    if account_invoice[0].invoice_line_ids[0].price_total:
                        opening_debit = account_invoice[0].invoice_line_ids[0].price_total
                    else: opening_debit = 0
                    opening_balance = initial_balance + account_move_lines[0].debit - account_move_lines[0].credit
                    opening_credit = account_move_lines[0].credit
                    new_opening_balance = opening_balance - opening_debit +opening_credit
                    sheet.write(7, 8, new_opening_balance, format1)
                    row += 1

                    for move in account_move_lines:
                        if True:
                            total_credit += move.credit
                            total_debit += move.debit
                            # initial_balance = initial_balance + move.debit - move.credit
                            # cre = convert_to_words(total_credit)
                            # deb = convert_to_words(total_debit)
                            # bal = convert_to_words(initial_balance)

                            sheet.write(row, 0, str(move.date), format1)
                            sheet.write(row, 1, move.move_id.name, format1)
                            sheet.set_column(row, 1, 25)
                            # sheet.write(row, 3, move.ref or "", format1)
                            # sheet.write(row, 4, move.name or "", format1)
                            # sheet.write(row, 2, '', format1)
                            # sheet.write(row, 3, '', format1)
                            # sheet.write(row, 4, '', format1)
                            # sheet.write(row, 5, '', format1)
                            if move.ref:
                                sheet.write(row, 5, move.ref, format1)
                            else:
                                sheet.write(row, 5, "", format1)
                            balance = initial_balance + move.debit - move.credit
                            # sheet.write(row, 7, move.debit, format1)
                            sheet.write(row, 7, move.credit, format1)
                            sheet.write(row, 8, balance, format1)
                            initial_balance = balance
                            # row += 1
                            account_invoice = self.env['account.move'].sudo().search(
                                [('id', '=', move.move_id.id), ('state', '=', 'posted'), ], limit=1)
                            if account_invoice:
                                if account_invoice.invoice_line_ids.product_id:
                                    num_lines = len(account_invoice.invoice_line_ids)  # عدد الأصناف في الفاتورة
                                    if num_lines > 1:
                                        sheet.merge_range(row, 1, row + num_lines - 1, 1, move.move_id.name, format1)
                                        sheet.merge_range(row, 0, row + num_lines - 1, 0, str(move.date), format1)
                                    else:
                                        sheet.write(row, 1, move.move_id.name, format1)
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
                                        sheet.write(row, 2, line.product_id.name, format1)
                                        sheet.write(row, 3, line.quantity, format1)
                                        sheet.write(row, 4, line.price_unit, format1)
                                        if line.move_id.type == 'out_refund':
                                            sheet.write(row, 6, '', format1)
                                        else:
                                            sheet.write(row, 6, line.price_total, format1)
                                        # sheet.write(row, 6, account_invoice.ref, format1)
                                        row += 1
                                    # row += 1
                                # elif 'INV' not in move.move_id.name:
                                elif move.payment_id:
                                    # sheet.write(row, 3, "الرقم", format1)
                                    # sheet.set_column(row, 3, 40)
                                    # sheet.write(row, 4, 'التاريخ', format1)
                                    # sheet.write(row, 5, 'المبلغ', format1)
                                    # sheet.write(row, 6, 'البنك', format1)
                                    # sheet.write(row, 5, 'Drawer Name', format1)
                                    row += 1
                                    for check in move.payment_id.payment_check_lines:
                                        sheet.write(row, 2, check.check_number, format2)
                                        sheet.write(row, 3, str(check.check_date), format2)
                                        sheet.write(row, 4, check.check_amount, format2)
                                        sheet.write(row, 5, check.check_bank_id.name, format2)
                                        # sheet.write(row, 6, check.communication, format2)
                                        # sheet.write(row, 5, check.with_drawer_name, format2)
                                        row += 1
                                else:
                                    sheet.write(row, 1, move.move_id.name, format1)
                                    row += 1

                    # sheet.write(row, 6, "رصيد المدين", format2)
                    # sheet.write(row + 1, 6, "رصيد الدائن", format2)
                    # sheet.write(row + 2, 6, "رصيد الرصيد", format2)
                    # sheet.write(row, 8, deb, format4)
                    # sheet.write(row + 1, 9, cre, format4)
                    # sheet.write(row + 2, 10, bal, format4)
                    # sheet.write(row, 7, total_debit, format3)
                    # sheet.write(row + 1, 8, total_credit, format3)
                    # sheet.write(row + 2, 9, balance, format3)

                    row += 7
