# -*- coding: utf-8 -*-
# from odoo import http


# class EnhanceOvertime(http.Controller):
#     @http.route('/enhance_overtime/enhance_overtime/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/enhance_overtime/enhance_overtime/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('enhance_overtime.listing', {
#             'root': '/enhance_overtime/enhance_overtime',
#             'objects': http.request.env['enhance_overtime.enhance_overtime'].search([]),
#         })

#     @http.route('/enhance_overtime/enhance_overtime/objects/<model("enhance_overtime.enhance_overtime"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('enhance_overtime.object', {
#             'object': obj
#         })
