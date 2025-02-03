# -*- coding: utf-8 -*-
# from odoo import http


# class ReportTimeOf(http.Controller):
#     @http.route('/report_time_of/report_time_of/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_time_of/report_time_of/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_time_of.listing', {
#             'root': '/report_time_of/report_time_of',
#             'objects': http.request.env['report_time_of.report_time_of'].search([]),
#         })

#     @http.route('/report_time_of/report_time_of/objects/<model("report_time_of.report_time_of"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_time_of.object', {
#             'object': obj
#         })
