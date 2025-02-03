# -*- coding: utf-8 -*-
# from odoo import http


# class AddFieldsAttendence(http.Controller):
#     @http.route('/add_fields_attendence/add_fields_attendence/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/add_fields_attendence/add_fields_attendence/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('add_fields_attendence.listing', {
#             'root': '/add_fields_attendence/add_fields_attendence',
#             'objects': http.request.env['add_fields_attendence.add_fields_attendence'].search([]),
#         })

#     @http.route('/add_fields_attendence/add_fields_attendence/objects/<model("add_fields_attendence.add_fields_attendence"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('add_fields_attendence.object', {
#             'object': obj
#         })
