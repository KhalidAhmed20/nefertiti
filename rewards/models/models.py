# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class rewards(models.Model):
    _name = 'rewards'
    _description = 'Rewards'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_ids'

    refrence  =  fields.Char(string="Reward No", readonly=True, required=True, copy=False, default='New')
    @api.model
    def create(self, vals):
        if vals.get('refrence', 'New') == 'New':
            vals['refrence'] = self.env['ir.sequence'].next_by_code(
                'rewards') or 'New'
        result = super(rewards, self).create(vals)
        return result

    employee_ids = fields.Many2one('hr.employee', string='Employee Name', required=True, help="Employee",tracking=True)
    datee = fields.Date(string='Date', default=fields.Date.today(),tracking=True)
    departments = fields.Many2one('hr.department', string='Department', readonly=True,tracking=True)
    amounts = fields.Float(string="Amount", required=True,tracking=True )
    payslip_id = fields.Many2one(comodel_name="hr.payslip", string="payslip_id", required=False, tracking=True)


class HrPayslipinherit(models.Model):
    _inherit = 'hr.payslip'

    rewards_ids = fields.One2many(comodel_name="rewards", inverse_name="payslip_id",
                                      string="Rewards",
                                      required=False, readonly=True, compute='get_rewards_ids')

    @api.model
    def _get_default_requested_by(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1)

    @api.depends('employee_id', 'date_from', 'date_to', )
    def get_rewards_ids(self):
        for rec in self:
            rec.rewards_ids = rec.rewards_ids
            rewards = self.env['rewards'].sudo().search(
                [('employee_ids', '=', self.employee_id.id), ('datee', '>=', self.date_from),
                 ('datee', '<=', self.date_to)])
            print('rewards', rewards)
            if rewards:
                rec.rewards_ids = rewards.mapped('id')
            else:
                rec.rewards_ids = rec.rewards_ids

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
