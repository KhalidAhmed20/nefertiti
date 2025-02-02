# -*- coding: utf-8 -*-
# from odoo import http


# class Edit-purches-order(http.Controller):
#     @http.route('/sequence-product-category/sequence-product-category/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sequence-product-category/sequence-product-category/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sequence-product-category.listing', {
#             'root': '/sequence-product-category/sequence-product-category',
#             'objects': http.request.env['sequence-product-category.sequence-product-category'].search([]),
#         })

#     @http.route('/sequence-product-category/sequence-product-category/objects/<model("sequence-product-category.sequence-product-category"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sequence-product-category.object', {
#             'object': obj
#         })
