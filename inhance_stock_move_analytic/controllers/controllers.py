# -*- coding: utf-8 -*-
# from odoo import http


# class InhanceStockMoveAnalytic(http.Controller):
#     @http.route('/inhance_stock_move_analytic/inhance_stock_move_analytic/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inhance_stock_move_analytic/inhance_stock_move_analytic/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inhance_stock_move_analytic.listing', {
#             'root': '/inhance_stock_move_analytic/inhance_stock_move_analytic',
#             'objects': http.request.env['inhance_stock_move_analytic.inhance_stock_move_analytic'].search([]),
#         })

#     @http.route('/inhance_stock_move_analytic/inhance_stock_move_analytic/objects/<model("inhance_stock_move_analytic.inhance_stock_move_analytic"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inhance_stock_move_analytic.object', {
#             'object': obj
#         })
