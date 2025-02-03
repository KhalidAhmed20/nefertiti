# -*- coding: utf-8 -*-
# from odoo import http


# class Adjustments(http.Controller):
#     @http.route('/adjustments/adjustments/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/adjustments/adjustments/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('adjustments.listing', {
#             'root': '/adjustments/adjustments',
#             'objects': http.request.env['adjustments.adjustments'].search([]),
#         })

#     @http.route('/adjustments/adjustments/objects/<model("adjustments.adjustments"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('adjustments.object', {
#             'object': obj
#         })
