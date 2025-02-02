# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class adjustments(models.Model):
    _name = 'adjustments.adjustments'
    _description = 'adjustments.adjustments'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    refrence  =  fields.Char(string="Adjustment Refrence NO", readonly=True, required=True, copy=False, default='New')
    @api.model
    def create(self, vals):
        if vals.get('refrence', 'New') == 'New':
            vals['refrence'] = self.env['ir.sequence'].next_by_code(
                'adjustments.adjustments') or 'New'
        result = super(adjustments, self).create(vals)
        return result
    employee_ids = fields.Many2one('hr.employee', string='Employee Name', required=True, help="Employee")
    datee = fields.Date(string='Date', default=fields.Date.today())
    departments = fields.Many2one('hr.department', string='Department', readonly=True)
    amounts = fields.Float(string="Amount", required=True, )
    payslip_id = fields.Many2one(comodel_name="hr.payslip", string="payslip_id", required=False, )


class HrPayslipEdit(models.Model):
    _inherit = 'hr.payslip'

    adjustments_ids = fields.One2many(comodel_name="adjustments.adjustments", inverse_name="payslip_id",
                                      string="Adjustments",
                                      required=False, readonly=True, compute='get_adjustments_ids')

    @api.model
    def _get_default_requested_by(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)

    @api.depends('employee_id', 'date_from', 'date_to', )
    def get_adjustments_ids(self):
        for rec in self:
            rec.adjustments_ids = rec.adjustments_ids
            adjustmentss = self.env['adjustments.adjustments'].sudo().search(
                [('employee_ids', '=', self.employee_id.id), ('datee', '>=', self.date_from),
                 ('datee', '<=', self.date_to)])
            print('adjustments', adjustmentss)
            if adjustmentss:
                rec.adjustments_ids = adjustmentss.mapped('id')
            else:
                rec.adjustments_ids = rec.adjustments_ids

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
