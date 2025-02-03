# -*- coding: utf-8 -*-
# from odoo import http


# class AddAchrive(http.Controller):
#     @http.route('/add_achrive/add_achrive/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/add_achrive/add_achrive/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('add_achrive.listing', {
#             'root': '/add_achrive/add_achrive',
#             'objects': http.request.env['add_achrive.add_achrive'].search([]),
#         })

#     @http.route('/add_achrive/add_achrive/objects/<model("add_achrive.add_achrive"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('add_achrive.object', {
#             'object': obj
#         })
