# -*- coding: utf-8 -*-
# from odoo import http


# class EditUnitPriceInPurchase(http.Controller):
#     @http.route('/edit_unit_price_in_purchase/edit_unit_price_in_purchase/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/edit_unit_price_in_purchase/edit_unit_price_in_purchase/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('edit_unit_price_in_purchase.listing', {
#             'root': '/edit_unit_price_in_purchase/edit_unit_price_in_purchase',
#             'objects': http.request.env['edit_unit_price_in_purchase.edit_unit_price_in_purchase'].search([]),
#         })

#     @http.route('/edit_unit_price_in_purchase/edit_unit_price_in_purchase/objects/<model("edit_unit_price_in_purchase.edit_unit_price_in_purchase"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('edit_unit_price_in_purchase.object', {
#             'object': obj
#         })
