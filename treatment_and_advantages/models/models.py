# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class treatment_advantages(models.Model):
    _name = 'treatment.advantages'
    _description = 'Treatment & advantages'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_ids'
    
    refrence  =  fields.Char(string="Reward No", readonly=True, required=True, copy=False, default='New')
    @api.model
    def create(self, vals):
        if vals.get('refrence', 'New') == 'New':
            vals['refrence'] = self.env['ir.sequence'].next_by_code(
                'treatment.advantages') or 'New'
        result = super(treatment_advantages, self).create(vals)
        return result

    employee_ids = fields.Many2one('hr.employee', string='Employee Name', required=True, help="Employee",tracking=True)
    datee = fields.Date(string='Date', default=fields.Date.today(),tracking=True)
    departments = fields.Many2one('hr.department', string='Department', readonly=True,tracking=True)
    amounts = fields.Float(string="Amount", required=True,tracking=True )
    payslip_id = fields.Many2one(comodel_name="hr.payslip", string="payslip_id", required=False, tracking=True)


class HrPayslipinheritTreatmentAdvantages(models.Model):
    _inherit = 'hr.payslip'

    treatment_advantages_ids = fields.One2many(comodel_name="treatment.advantages", inverse_name="payslip_id",
                                      string="علاج و مزايا",
                                      required=False, readonly=True, compute='get_treatment_advantages_ids')

    @api.model
    def _get_default_requested_by(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)

    @api.depends('employee_id', 'date_from', 'date_to', )
    def get_treatment_advantages_ids(self):
        for rec in self:
            rec.treatment_advantages_ids = rec.treatment_advantages_ids
            treatment_advantages = self.env['treatment.advantages'].sudo().search(
                [('employee_ids', '=', self.employee_id.id), ('datee', '>=', self.date_from),
                 ('datee', '<=', self.date_to)])
            print('treatment_advantages', treatment_advantages)
            if treatment_advantages:
                rec.treatment_advantages_ids = treatment_advantages.mapped('id')
            else:
                rec.treatment_advantages_ids = rec.treatment_advantages_ids

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
