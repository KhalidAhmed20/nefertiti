# -*- coding: utf-8 -*-
# from odoo import http


# class HrEmployeeAddedFields(http.Controller):
#     @http.route('/hr_employee_added_fields/hr_employee_added_fields/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_employee_added_fields/hr_employee_added_fields/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_employee_added_fields.listing', {
#             'root': '/hr_employee_added_fields/hr_employee_added_fields',
#             'objects': http.request.env['hr_employee_added_fields.hr_employee_added_fields'].search([]),
#         })

#     @http.route('/hr_employee_added_fields/hr_employee_added_fields/objects/<model("hr_employee_added_fields.hr_employee_added_fields"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_employee_added_fields.object', {
#             'object': obj
#         })
