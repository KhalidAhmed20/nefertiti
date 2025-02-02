# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class ReportStockCardReportXlsx(models.AbstractModel):
    _name = "report.stock_card_report.report_stock_card_report_xlsx"
    _description = "Stock Card Report XLSX"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, objects):
        self._define_formats(workbook)
        for product in objects.product_ids:
            for ws_params in self._get_ws_params(workbook, data, product):
                ws_name = ws_params.get("ws_name")
                ws_name = self._check_ws_name(ws_name)
                ws = workbook.add_worksheet(ws_name)
                ws.right_to_left()
                format_merge = workbook.add_format({'align': 'center', 'bold': True})
                ws.merge_range(4, 4, 4, 5, 'الوارد', format_merge)
                ws.merge_range(4, 6, 4, 7, 'الصادر', format_merge)
                generate_ws_method = getattr(self, ws_params["generate_ws_method"])
                generate_ws_method(workbook, ws, ws_params, data, objects, product)

    def _get_ws_params(self, wb, data, product):
        filter_template = {
            "1_date_from": {
                "header": {"value": "من"},
                "data": {
                    "value": self._render("date_from"),
                    "format": self.format_tcell_date_center,
                },
            },
            "2_date_to": {
                "header": {"value": "الى"},
                "data": {
                    "value": self._render("date_to"),
                    "format": self.format_tcell_date_center,
                },
            },
            "3_location": {
                "header": {"value": "المكان"},
                "data": {
                    "value": self._render("location"),
                    "format": self.format_tcell_center,
                },
            },
        }
        initial_template = {
            "1_ref": {
                "data": {"value": "Initial", "format": self.format_tcell_center},
                "colspan": 4,
            },
            "2_white": {
                "data": {
                    "value": "",
                    "format": self.format_tcell_amount_right,
                },
                "colspan": 4,
            },
            "3_balance": {
                "data": {
                    "value": self._render("balance"),
                    "format": self.format_tcell_amount_right,
                }
            },
        }
        stock_card_template = {
            "1_date": {
                "header": {"value": "التاريخ"},
                "data": {
                    "value": self._render("date"),
                    "format": self.format_tcell_date_left,
                },
                "width": 25,
            },
            "2_references": {
                "header": {"value": "رقم العملية"},
                "data": {
                    "value": self._render("move_reference"),
                    "format": self.format_tcell_left,
                },
                "width": 25,
            },
            "2_reference": {
                "header": {"value": "البيان"},
                "data": {
                    "value": self._render("reference"),
                    "format": self.format_tcell_left,
                },
                "width": 25,
            },
            "3_average": {
                "header": {"value": "سعر الوحدة"},
                "data": {"value": self._render("average")},
                "width": 25,
            },
            "4_input": {
                "header": {"value": "وارد"},
                "data": {"value": self._render("input")},
                "width": 25,
            },
            "5_amount_input": {
                "header": {"value": "تكلفة الوارد"},
                "data": {"value": self._render("amount_input")},
                "width": 25,
            },
            "6_output": {
                "header": {"value": "صادر"},
                "data": {"value": self._render("output")},
                "width": 25,
            },
            "7_amount_output": {
                "header": {"value": "تكلفة الصادر"},
                "data": {"value": self._render("amount_output")},
                "width": 25,
            },
            "8_balance": {
                "header": {"value": "رصيد"},
                "data": {"value": self._render("balance")},
                "width": 25,
            },
            "9_amount_balance": {
                "header": {"value": "تكلفة الرصيد"},
                "data": {"value": self._render("amount_balance")},
                "width": 25,
            },
        }

        ws_params = {
            "ws_name": product.name,
            "generate_ws_method": "_stock_card_report",
            "title": "Stock Card - {}".format(product.name),
            "wanted_list_filter": [k for k in sorted(filter_template.keys())],
            "col_specs_filter": filter_template,
            "wanted_list_initial": [k for k in sorted(initial_template.keys())],
            "col_specs_initial": initial_template,
            "wanted_list": [k for k in sorted(stock_card_template.keys())],
            "col_specs": stock_card_template,
        }
        return [ws_params]

    def _stock_card_report(self, wb, ws, ws_params, data, objects, product):
        ws.set_portrait()
        ws.fit_to_pages(1, 0)
        ws.set_header(self.xls_headers["standard"])
        ws.set_footer(self.xls_footers["standard"])
        self._set_column_width(ws, ws_params)
        # Title
        row_pos = 0
        row_pos = self._write_ws_title(ws, row_pos, ws_params, True)
        # Filter Table
        row_pos = self._write_line(
            ws,
            row_pos,
            ws_params,
            col_specs_section="header",
            default_format=self.format_theader_blue_center,
            col_specs="col_specs_filter",
            wanted_list="wanted_list_filter",
        )
        row_pos = self._write_line(
            ws,
            row_pos,
            ws_params,
            col_specs_section="data",
            render_space={
                "date_from": objects.date_from or "",
                "date_to": objects.date_to or "",
                "location": objects.location_id.display_name or "",
            },
            col_specs="col_specs_filter",
            wanted_list="wanted_list_filter",
        )
        row_pos += 1
        # Stock Card Table
        row_pos = self._write_line(
            ws,
            row_pos,
            ws_params,
            col_specs_section="header",
            default_format=self.format_theader_blue_center,
        )
        ws.freeze_panes(row_pos, 0)
        balance = objects._get_initial(
            objects.results.filtered(lambda l: l.product_id == product and l.is_initial)
        )
        row_pos = self._write_line(
            ws,
            row_pos,
            ws_params,
            col_specs_section="data",
            render_space={"balance": balance},
            col_specs="col_specs_initial",
            wanted_list="wanted_list_initial",
        )
        product_lines = objects.results.filtered(
            lambda l: l.product_id == product and not l.is_initial
        )
        price = 0
        total_price = 0
        total_input = 0
        total_output = 0
        total_balance = balance
        for line in product_lines:
            balance += line.product_in - line.product_out
            for l in line.move_id.account_move_ids:
                price = l.amount_total_signed / line.product_qty
            # balance += line.product_in - line.product_out
            total_price += price
            total_input += line.product_in or 0
            total_output += line.product_out or 0
            total_balance += balance
            move_ref = ""
            if line.move_id.picking_id:
                if line.move_id.picking_id.sale_id:
                    move_ref = line.move_id.picking_id.sale_id.name
                elif line.move_id.picking_id.purchase_id:
                    move_ref = line.move_id.picking_id.purchase_id.name
                else:
                    print(55)
            row_pos = self._write_line(
                ws,
                row_pos,
                ws_params,
                col_specs_section="data",
                render_space={
                    "date": line.date or "",
                    "move_reference": move_ref or "",
                    "reference": line.reference or "",
                    "average": price,
                    "input": line.product_in or 0,
                    "amount_input": price * line.product_in,
                    "output": line.product_out or 0,
                    "amount_output": price * line.product_out,
                    "balance": balance,
                    "amount_balance": price * balance,
                },
                default_format=self.format_tcell_amount_right,
            )
        row_pos = self._write_line(
            ws,
            row_pos,
            ws_params,
            col_specs_section="data",
            render_space={
                "date": "",
                "move_reference": "",
                "reference": "الإجمالي",
                "average": total_price,
                "input": total_input or 0,
                "amount_input": total_price * total_input,
                "output": total_output or 0,
                "amount_output": total_price * total_output,
                "balance": total_balance,
                "amount_balance": total_price * total_balance,
            },
            default_format=self.format_tcell_amount_right,
        )
