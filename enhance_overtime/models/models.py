# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError



class HrOverTime(models.Model):
    _inherit = 'hr.overtime'

    hour_type_bonus = fields.Selection([('b_6', 'تطبيق ليلى'),
                                        ('b_9', 'تطبيق نهارى')],
                                       required=True, )
    over_hours = fields.Float(string="total Over Time Hours", compute='compute_over_hours')
                              # compute='compute_over_hours')
    new_field = fields.Char(string="", required=False, compute='compute_over_hours')

    @api.depends('hour_type_bonus', 'days_no_tmp')
    def compute_over_hours(self):
        for rec in self:
            if rec.hour_type_bonus == 'b_3':
                rec.over_hours = rec.days_no_tmp * 1.35
                rec.new_field = "Mohamed"
            elif rec.hour_type_bonus == 'b_4':
                rec.over_hours = rec.days_no_tmp * 1.70
                rec.new_field = "Mohamed"
            elif rec.hour_type_bonus == 'b_5':
                rec.over_hours = rec.days_no_tmp * 1
                rec.new_field = "Mohamed"
            elif rec.hour_type_bonus == 'b_6':
                rec.over_hours = rec.days_no_tmp * 1.5
                rec.new_field = "Mohamed"
            elif rec.hour_type_bonus == 'b_7':
                rec.over_hours = rec.days_no_tmp * 1.35
                rec.new_field = "Mohamed"
            elif rec.hour_type_bonus == 'b_8':
                rec.over_hours = rec.days_no_tmp * 1.70
                rec.new_field = "Mohamed"
            elif rec.hour_type_bonus == 'b_9':
                rec.over_hours = rec.days_no_tmp * 1.25
                rec.new_field = "Mohamed"
            else:
                rec.over_hours = 0.0
                rec.new_field = "Mohamed"


    def recipt_to_draft(self):
        for rec in self:
            rec.state = 'draft'

class hr_leave(models.Model):
    _inherit = 'hr.leave'


    request_hour_from = fields.Float(string="Hour From", required=False, )
    request_hour_to = fields.Float(string="Hour To", required=False, )
    duration_hour = fields.Float(string="Duration",  required=False, )



    @api.onchange('request_hour_from', 'request_hour_to')
    def get_duration(self):
        for rec in self:
            rec.duration_hour = float(rec.request_hour_to) - float(rec.request_hour_from)

