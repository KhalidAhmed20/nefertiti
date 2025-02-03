# -*- coding: utf-8 -*-
# from odoo import http


# class EditDateInModelsOdoo(http.Controller):
#     @http.route('/edit_date_in_models_odoo/edit_date_in_models_odoo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/edit_date_in_models_odoo/edit_date_in_models_odoo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('edit_date_in_models_odoo.listing', {
#             'root': '/edit_date_in_models_odoo/edit_date_in_models_odoo',
#             'objects': http.request.env['edit_date_in_models_odoo.edit_date_in_models_odoo'].search([]),
#         })

#     @http.route('/edit_date_in_models_odoo/edit_date_in_models_odoo/objects/<model("edit_date_in_models_odoo.edit_date_in_models_odoo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('edit_date_in_models_odoo.object', {
#             'object': obj
#         })
