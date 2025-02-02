# -*- coding: utf-8 -*-
# from odoo import http


# class ReportMrp(http.Controller):
#     @http.route('/report_mrp/report_mrp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_mrp/report_mrp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_mrp.listing', {
#             'root': '/report_mrp/report_mrp',
#             'objects': http.request.env['report_mrp.report_mrp'].search([]),
#         })

#     @http.route('/report_mrp/report_mrp/objects/<model("report_mrp.report_mrp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_mrp.object', {
#             'object': obj
#         })
