# -*- coding: utf-8 -*-
# from odoo import http


# class TheValueAddedTax(http.Controller):
#     @http.route('/the_value_added_tax/the_value_added_tax/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/the_value_added_tax/the_value_added_tax/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('the_value_added_tax.listing', {
#             'root': '/the_value_added_tax/the_value_added_tax',
#             'objects': http.request.env['the_value_added_tax.the_value_added_tax'].search([]),
#         })

#     @http.route('/the_value_added_tax/the_value_added_tax/objects/<model("the_value_added_tax.the_value_added_tax"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('the_value_added_tax.object', {
#             'object': obj
#         })
