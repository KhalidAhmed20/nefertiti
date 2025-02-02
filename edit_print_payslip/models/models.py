# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class edit_print_payslip(models.Model):
#     _name = 'edit_print_payslip.edit_print_payslip'
#     _description = 'edit_print_payslip.edit_print_payslip'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
