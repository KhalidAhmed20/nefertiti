# -*- coding: utf-8 -*-
# from odoo import http


# class HrNevertity(http.Controller):
#     @http.route('/hr_nevertity/hr_nevertity/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_nevertity/hr_nevertity/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_nevertity.listing', {
#             'root': '/hr_nevertity/hr_nevertity',
#             'objects': http.request.env['hr_nevertity.hr_nevertity'].search([]),
#         })

#     @http.route('/hr_nevertity/hr_nevertity/objects/<model("hr_nevertity.hr_nevertity"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_nevertity.object', {
#             'object': obj
#         })
