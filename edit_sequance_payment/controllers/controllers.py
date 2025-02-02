# -*- coding: utf-8 -*-
# from odoo import http


# class EditSequancePayment(http.Controller):
#     @http.route('/edit_sequance_payment/edit_sequance_payment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/edit_sequance_payment/edit_sequance_payment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('edit_sequance_payment.listing', {
#             'root': '/edit_sequance_payment/edit_sequance_payment',
#             'objects': http.request.env['edit_sequance_payment.edit_sequance_payment'].search([]),
#         })

#     @http.route('/edit_sequance_payment/edit_sequance_payment/objects/<model("edit_sequance_payment.edit_sequance_payment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('edit_sequance_payment.object', {
#             'object': obj
#         })
