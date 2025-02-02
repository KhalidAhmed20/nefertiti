# -*- coding: utf-8 -*-
# from odoo import http


# class Edit-purches-order(http.Controller):
#     @http.route('/edit-purches-order/edit-purches-order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/edit-purches-order/edit-purches-order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('edit-purches-order.listing', {
#             'root': '/edit-purches-order/edit-purches-order',
#             'objects': http.request.env['edit-purches-order.edit-purches-order'].search([]),
#         })

#     @http.route('/edit-purches-order/edit-purches-order/objects/<model("edit-purches-order.edit-purches-order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('edit-purches-order.object', {
#             'object': obj
#         })
