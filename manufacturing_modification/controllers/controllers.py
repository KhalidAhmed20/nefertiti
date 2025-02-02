# -*- coding: utf-8 -*-
# from odoo import http


# class ManufacturingModification(http.Controller):
#     @http.route('/manufacturing_modification/manufacturing_modification/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/manufacturing_modification/manufacturing_modification/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('manufacturing_modification.listing', {
#             'root': '/manufacturing_modification/manufacturing_modification',
#             'objects': http.request.env['manufacturing_modification.manufacturing_modification'].search([]),
#         })

#     @http.route('/manufacturing_modification/manufacturing_modification/objects/<model("manufacturing_modification.manufacturing_modification"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('manufacturing_modification.object', {
#             'object': obj
#         })
