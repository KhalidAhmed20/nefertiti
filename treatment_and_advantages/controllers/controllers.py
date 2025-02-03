# -*- coding: utf-8 -*-
# from odoo import http


# class Rewards(http.Controller):
#     @http.route('/rewards/rewards/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rewards/rewards/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rewards.listing', {
#             'root': '/rewards/rewards',
#             'objects': http.request.env['rewards.rewards'].search([]),
#         })

#     @http.route('/rewards/rewards/objects/<model("rewards.rewards"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rewards.object', {
#             'object': obj
#         })
