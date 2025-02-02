# -*- coding: utf-8 -*-
# from odoo import http


# class PoDeliveryTerms(http.Controller):
#     @http.route('/po_delivery_terms/po_delivery_terms/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/po_delivery_terms/po_delivery_terms/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('po_delivery_terms.listing', {
#             'root': '/po_delivery_terms/po_delivery_terms',
#             'objects': http.request.env['po_delivery_terms.po_delivery_terms'].search([]),
#         })

#     @http.route('/po_delivery_terms/po_delivery_terms/objects/<model("po_delivery_terms.po_delivery_terms"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('po_delivery_terms.object', {
#             'object': obj
#         })
