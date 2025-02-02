# -*- coding: utf-8 -*-
# from odoo import http


# class ReportDelivery(http.Controller):
#     @http.route('/report_delivery/report_delivery/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_delivery/report_delivery/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_delivery.listing', {
#             'root': '/report_delivery/report_delivery',
#             'objects': http.request.env['report_delivery.report_delivery'].search([]),
#         })

#     @http.route('/report_delivery/report_delivery/objects/<model("report_delivery.report_delivery"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_delivery.object', {
#             'object': obj
#         })
