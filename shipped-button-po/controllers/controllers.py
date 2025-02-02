# -*- coding: utf-8 -*-
# from odoo import http


# class Shipped-button-po(http.Controller):
#     @http.route('/shipped-button-po/shipped-button-po/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/shipped-button-po/shipped-button-po/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('shipped-button-po.listing', {
#             'root': '/shipped-button-po/shipped-button-po',
#             'objects': http.request.env['shipped-button-po.shipped-button-po'].search([]),
#         })

#     @http.route('/shipped-button-po/shipped-button-po/objects/<model("shipped-button-po.shipped-button-po"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('shipped-button-po.object', {
#             'object': obj
#         })
