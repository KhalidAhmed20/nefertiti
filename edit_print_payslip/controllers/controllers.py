# -*- coding: utf-8 -*-
# from odoo import http


# class EditPrintPayslip(http.Controller):
#     @http.route('/edit_print_payslip/edit_print_payslip/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/edit_print_payslip/edit_print_payslip/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('edit_print_payslip.listing', {
#             'root': '/edit_print_payslip/edit_print_payslip',
#             'objects': http.request.env['edit_print_payslip.edit_print_payslip'].search([]),
#         })

#     @http.route('/edit_print_payslip/edit_print_payslip/objects/<model("edit_print_payslip.edit_print_payslip"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('edit_print_payslip.object', {
#             'object': obj
#         })
