# -*- coding: utf-8 -*-


from odoo import _, api, fields, models


class GeneralLedgerAccount(models.AbstractModel):
    _name = 'report.report_inventory_location.report_location'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        for obj in partners:
            report_name = obj.name
            # One sheet by partner
            sheet = workbook.add_worksheet('Location Report')
            sheet.set_column('A:A', 25)
            sheet.set_column('B:B', 30)
            sheet.set_column('C:C', 30)
            sheet.set_column('D:D', 30)
            sheet.set_column('E:E', 13)
            sheet.set_column('F:F', 13)
            sheet.set_column('G:G', 13)
            sheet.set_column('H:H', 13)
            sheet.set_column('J:J', 13)
            format0 = workbook.add_format({'font_size': 15, 'align': 'center'})
            format1 = workbook.add_format(
                {'font_size': 15, 'align': 'center', 'bold': True, 'bg_color': '#D5D5D5', 'color': 'black',
                 'border': 2})
            format2 = workbook.add_format(
                {'font_size': 13, 'align': 'center', 'bold': True,
                 'border': 1})
            format10 = workbook.add_format({'align': 'center', 'bold': True, 'bg_color': '#FF6600', 'border': 5})
            format3 = workbook.add_format(
                {'align': 'center', 'bold': True, 'bg_color': '#4CE400', 'color': 'black', 'border': 5})
            row = 1
            sheet.merge_range(row, 2, row, 6, 'Stock Move', format3)
            row += 3
            sheet.write(row, 2, 'FROM : ' + str(obj.date_from), format0)
            sheet.write(row, 5, 'TO : ' + str(obj.date_to), format0)
            row += 2
            if obj.location_ids:
                for location in obj.location_ids:

                    list = []
                    pickings1 = self.env['stock.picking'].sudo().search([
                        ('location_id', '=', location.id),
                        # ('location_dest_id', '=', location.id),
                        ('date','>=', obj.date_from),
                        ('date','<=', obj.date_to),
                    ]).mapped('id')
                    # list.append(pickings1.mapped)
                    pickings2 = self.env['stock.picking'].sudo().search([
                        # ('location_id', '=', location.id),
                        ('location_dest_id', '=', location.id),
                        ('date','>=', obj.date_from),
                        ('date','<=', obj.date_to),
                    ]).mapped('id')
                    pickings2.extend(pickings1)
                    pickings = self.env['stock.picking'].sudo().search([
                        ('id', 'in', pickings2),
                    ], order="date ASC")
                    print('kkkkkkkkkkkkkk',pickings)
                    if pickings:
                        sheet.merge_range(row, 2, row, 6, str(location.location_id.name)+'/'+str(location.name), format1)
                        row += 2
                        sheet.write(row, 1, 'Date', format3)
                        sheet.write(row, 2, 'From', format3)
                        sheet.write(row, 3, 'To', format3)
                        sheet.write(row, 4, 'Reference', format3)
                        sheet.write(row, 5, 'Product', format3)
                        sheet.write(row, 6, 'Quantity demand', format3)
                        sheet.write(row, 7, 'Quantity Done', format3)
                        sheet.write(row, 8, 'Status', format3)
                        row += 1
                        for picking in pickings:
                            for line in picking.move_ids_without_package:
                                sheet.write(row, 1, str(picking.date), format2)
                                sheet.write(row, 2, str(picking.location_id.location_id.name)+'/'+str(picking.location_id.name), format2)
                                sheet.write(row, 3, str(picking.location_dest_id.location_id.name)+'/'+str(picking.location_dest_id.name), format2)
                                sheet.write(row, 4, picking.name, format2)
                                sheet.write(row, 5, line.product_id.name, format2)
                                sheet.write(row, 6, line.product_uom_qty, format2)
                                sheet.write(row, 7, line.quantity_done, format2)
                                sheet.write(row, 8, picking.state, format2)
                                row+=1
                        row+=1

