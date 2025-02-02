# -*- coding: utf-8 -*-
# from odoo import http


# class EditTransfers(http.Controller):
#     @http.route('/edit_transfers/edit_transfers/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/edit_transfers/edit_transfers/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('edit_transfers.listing', {
#             'root': '/edit_transfers/edit_transfers',
#             'objects': http.request.env['edit_transfers.edit_transfers'].search([]),
#         })

#     @http.route('/edit_transfers/edit_transfers/objects/<model("edit_transfers.edit_transfers"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('edit_transfers.object', {
#             'object': obj
#         })
