# -*- coding: utf-8 -*-
# from odoo import http


# class AllowanceHrEmployee(http.Controller):
#     @http.route('/allowance_hr_employee/allowance_hr_employee/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/allowance_hr_employee/allowance_hr_employee/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('allowance_hr_employee.listing', {
#             'root': '/allowance_hr_employee/allowance_hr_employee',
#             'objects': http.request.env['allowance_hr_employee.allowance_hr_employee'].search([]),
#         })

#     @http.route('/allowance_hr_employee/allowance_hr_employee/objects/<model("allowance_hr_employee.allowance_hr_employee"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('allowance_hr_employee.object', {
#             'object': obj
#         })
