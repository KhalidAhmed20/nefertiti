# -*- coding: utf-8 -*-
# from odoo import http


# class AttendanceTreatment(http.Controller):
#     @http.route('/attendance_treatment/attendance_treatment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/attendance_treatment/attendance_treatment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('attendance_treatment.listing', {
#             'root': '/attendance_treatment/attendance_treatment',
#             'objects': http.request.env['attendance_treatment.attendance_treatment'].search([]),
#         })

#     @http.route('/attendance_treatment/attendance_treatment/objects/<model("attendance_treatment.attendance_treatment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('attendance_treatment.object', {
#             'object': obj
#         })
