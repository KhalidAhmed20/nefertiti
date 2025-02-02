# -*- coding: utf-8 -*-
# from odoo import http


# class EditOperationTypeVendor(http.Controller):
#     @http.route('/edit_operation_type_vendor/edit_operation_type_vendor/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/edit_operation_type_vendor/edit_operation_type_vendor/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('edit_operation_type_vendor.listing', {
#             'root': '/edit_operation_type_vendor/edit_operation_type_vendor',
#             'objects': http.request.env['edit_operation_type_vendor.edit_operation_type_vendor'].search([]),
#         })

#     @http.route('/edit_operation_type_vendor/edit_operation_type_vendor/objects/<model("edit_operation_type_vendor.edit_operation_type_vendor"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('edit_operation_type_vendor.object', {
#             'object': obj
#         })
