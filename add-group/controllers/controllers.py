# -*- coding: utf-8 -*-
# from odoo import http


# class Add-group(http.Controller):
#     @http.route('/add-group/add-group/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/add-group/add-group/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('add-group.listing', {
#             'root': '/add-group/add-group',
#             'objects': http.request.env['add-group.add-group'].search([]),
#         })

#     @http.route('/add-group/add-group/objects/<model("add-group.add-group"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('add-group.object', {
#             'object': obj
#         })
