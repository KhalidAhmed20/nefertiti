# -*- coding: utf-8 -*-
# from odoo import http


# class EditReportPurcheas(http.Controller):
#     @http.route('/edit_report_purcheas/edit_report_purcheas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/edit_report_purcheas/edit_report_purcheas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('edit_report_purcheas.listing', {
#             'root': '/edit_report_purcheas/edit_report_purcheas',
#             'objects': http.request.env['edit_report_purcheas.edit_report_purcheas'].search([]),
#         })

#     @http.route('/edit_report_purcheas/edit_report_purcheas/objects/<model("edit_report_purcheas.edit_report_purcheas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('edit_report_purcheas.object', {
#             'object': obj
#         })
