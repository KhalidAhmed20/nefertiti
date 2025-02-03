# -*- coding: utf-8 -*-
# from odoo import http


# class AddPricePivot(http.Controller):
#     @http.route('/add_price_pivot/add_price_pivot/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/add_price_pivot/add_price_pivot/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('add_price_pivot.listing', {
#             'root': '/add_price_pivot/add_price_pivot',
#             'objects': http.request.env['add_price_pivot.add_price_pivot'].search([]),
#         })

#     @http.route('/add_price_pivot/add_price_pivot/objects/<model("add_price_pivot.add_price_pivot"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('add_price_pivot.object', {
#             'object': obj
#         })
