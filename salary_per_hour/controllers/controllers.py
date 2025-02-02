# -*- coding: utf-8 -*-
# from odoo import http


# class SalaryPerHour(http.Controller):
#     @http.route('/salary_per_hour/salary_per_hour/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/salary_per_hour/salary_per_hour/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('salary_per_hour.listing', {
#             'root': '/salary_per_hour/salary_per_hour',
#             'objects': http.request.env['salary_per_hour.salary_per_hour'].search([]),
#         })

#     @http.route('/salary_per_hour/salary_per_hour/objects/<model("salary_per_hour.salary_per_hour"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('salary_per_hour.object', {
#             'object': obj
#         })
