# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    #hour_wage = fields.Float('Number Of Hours')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, readonly=True)
    hour_wage = fields.Monetary('Hour Wage', currency_field="currency_id", related='contract_id.over_hour',store=True)
    no_of_hours = fields.Float('Number Of Hours', related='line_ids.no_of_hours',store=True)

class  hrpayslipline(models.Model):
    _inherit = 'hr.payslip.line'
    
    #no_of_hours = fields.Float(related='slip_id.no_of_hours',store=True)

    #hour_wage = fields.Float('Hour Wage',compute='_get_hour_wage',store=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, readonly=True)
    hour_wage = fields.Monetary(related='slip_id.hour_wage', currency_field="currency_id", store=True)
    no_of_hours = fields.Float('Number Of Hours',compute='_get_no_of_hours',store=True)  

    @api.depends('hour_wage')
    def _get_no_of_hours(self):
        for rec in self:
            if rec.hour_wage:
                rec.no_of_hours = rec.amount / float(rec.hour_wage)
            else:
                rec.no_of_hours = False
