# -*- coding: utf-8 -*-
# from odoo import http


# class AddAnalyticAccountInventory(http.Controller):
#     @http.route('/add_analytic_account_inventory/add_analytic_account_inventory/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/add_analytic_account_inventory/add_analytic_account_inventory/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('add_analytic_account_inventory.listing', {
#             'root': '/add_analytic_account_inventory/add_analytic_account_inventory',
#             'objects': http.request.env['add_analytic_account_inventory.add_analytic_account_inventory'].search([]),
#         })

#     @http.route('/add_analytic_account_inventory/add_analytic_account_inventory/objects/<model("add_analytic_account_inventory.add_analytic_account_inventory"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('add_analytic_account_inventory.object', {
#             'object': obj
#         })
