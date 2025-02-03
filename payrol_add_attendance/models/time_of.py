# -*- coding: utf-8 -*-

from odoo import models, fields, api
import random
import datetime
from datetime import datetime, timedelta, date




class HrLeaveInherit(models.Model):
    _inherit = 'hr.leave'

    hr_payslip_id = fields.Many2one(comodel_name="hr.payslip", string="", required=False, )


class HrPaysLipInherit(models.Model):
    _inherit = 'hr.payslip'

    active = fields.Boolean(
        default=True, )

    # loan_ids = fields.One2many(comodel_name="loans", inverse_name="loan_id", string="", required=False,
    #                            compute='get_loan_ids')
    leave_payslip_ids = fields.One2many(comodel_name="hr.leave", inverse_name="hr_payslip_id", string="", required=False,
                               compute='get_leave_payslip_ids')
    # leaves = fields.Float(string="Leaves" , compute='get_total_leaves')




    @api.depends('employee_id', 'date_from', 'date_to', )
    def get_leave_payslip_ids(self):
        for rec in self:
            rec.leave_payslip_ids = False
            leaves = rec.env['hr.leave'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('state', '=', 'validate'),
                ('request_date_to', '<=', rec.date_to),
                ('request_date_from', '>=', rec.date_from),
                # ('loans_ids', '!=', False),
            ])
    
            if leaves:
                rec.leave_payslip_ids = leaves
            else:
                rec.leave_payslip_ids = False





    #
    # @api.depends('employee_id', 'date_from', 'date_to', )
    # def get_total_leaves(self):
    #     leaves_leaves=0
    #     for rec in self:
    #         rec.leaves=False
    #         if rec.leave_payslip_ids:
    #             for line in rec.leave_payslip_ids:
    #                 leaves_leaves=leaves_leaves+line.amount
    #             rec.loans=loan_loan
    #         else:
    #             rec.loans = False
    #




