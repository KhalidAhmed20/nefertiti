# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from datetime import datetime as dt, date
from time import time
import datetime
import pytz
from pytz import timezone
from odoo.exceptions import ValidationError, AccessError, MissingError, UserError
from dateutil.relativedelta import relativedelta


class NewModule(models.Model):
    _inherit = 'hr.attendance'

    actual_worked_hours = fields.Float(string='Actual Worked Hours', compute='get_actual_worked_hours', store=True, readonly=True)
    late = fields.Float(string='Late', compute='', store=True, readonly=True)
    over_time = fields.Float(string='Total Extra Hours')
    total_over_time = fields.Float(string='Total Over Time')
    net_over_time = fields.Float(string='Net Over Time')
    is_day_shift = fields.Selection(string="Is Day Shift", selection=[('day', 'Day'), ('night', 'Night'), ], required=False, )
    early_sign_in = fields.Float(string='Early Sign In')
    early_leave = fields.Float(string='Early Leave')
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date TO")
    hour_from = fields.Float(string="Hour From", compute="get_sheft")
    hour_to = fields.Float(string="Hour To", compute="get_sheft")
    worked_hours = fields.Float(string='Worked Hours', compute='_compute_worked_hours', store=True, readonly=True)

    @api.depends('worked_hours')
    def get_actual_worked_hours(self):
        for rec in self:
            if 11.5 <= rec.worked_hours <= 12 :
                rec.actual_worked_hours=12
            else:
                rec.actual_worked_hours=rec.worked_hours



    @api.depends('check_in', 'check_out')
    def _compute_worked_hours(self):
        for attendance in self:
            if attendance.check_out:
                delta = attendance.check_out - attendance.check_in
                if 12 < delta.total_seconds() / 3600.0 < 13:
                    attendance.worked_hours = 12
                else:
                    attendance.worked_hours = delta.total_seconds() / 3600.0
            else:
                attendance.worked_hours = False

    @api.depends('employee_id')
    def get_sheft(self):
        for rec in self:
            if rec.check_in and rec.check_out:
                shiftsh = self.env['employee.shift.line'].search(
                    [('shift_name_id', '=', rec.employee_id.id), ('date_from', '=', rec.check_in.date()), ('date_to', '=', rec.check_out.date())], limit=1)
                rec.date_from = shiftsh.date_from
                rec.date_to = shiftsh.date_to
                rec.hour_from = shiftsh.hour_from
                rec.hour_to = shiftsh.hour_to
                rec.is_day_shift = shiftsh.is_day_shift
            else:
                rec.date_from =  rec.date_from
                rec.date_to = rec.date_to
                rec.hour_from = rec.hour_from
                rec.hour_to = rec.hour_to
                rec.is_day_shift = rec.is_day_shift

    @api.onchange('check_in', 'check_out', 'hour_from', 'hour_to', 'is_day_shift', 'over_time', 'total_over_time', 'net_over_time')
    def compute_early_late(self):
        for rec in self:
            if rec.check_in:
                check_in_hour = rec.check_in.hour + (rec.check_in.minute / 60) + 2
                late_in = check_in_hour - rec.hour_from
                if late_in >= 0:
                    rec.late = late_in
                    rec.early_sign_in = 0
                else:
                    rec.early_sign_in = -late_in
                    rec.late = 0
            if rec.check_out:
                check_out_hour = rec.check_out.hour + (rec.check_out.minute / 60) + 2
                late_out = rec.hour_to - check_out_hour
                worked_hours = int(rec.worked_hours)
                if late_out >= 0:
                    rec.over_time = 0
                    if worked_hours <= 12:
                        rec.early_leave = late_out
                    else:
                        rec.early_leave = 0
                else:
                    rec.over_time = -late_out
                    rec.early_leave = 0
                    if rec.over_time >= 5:
                        rec.total_over_time = 5
                    else:
                        rec.total_over_time = rec.over_time
                    if rec.is_day_shift == "day":
                        rec.net_over_time = rec.total_over_time * rec.employee_id.co_officient_day_overtime
                    elif rec.is_day_shift == "night":
                        rec.net_over_time = rec.total_over_time * rec.employee_id.co_officient_night_overtime
                    else:
                        rec.net_over_time = 0

    def meshmesh(self):
        attendance = self.env['hr.attendance'].sudo().search([])
        for x in attendance:
            x.sudo().compute_early_late()

        # if self.check_in:
        # date_check_in = dt.strptime(str(self.check_in), '%Y-%m-%d %H:%M:%S').time()
        # planned_check_in = dt(1988, 2, 19, int(self.hour_from))
        # planned_check_in = planned_check_in.strftime('%H:%M:%S')
        # date_hour_from = dt.strptime(str(planned_check_in), '%H:%M:%S').time()
        # if date_hour_from < date_check_in:
        #     z = dt.combine(date.today(), date_check_in)  - dt.combine(date.today(), date_hour_from)
        # elif date_hour_from > date_check_in:
        #     z = dt.combine(date.today(), date_hour_from) - dt.combine(date.today(), date_check_in)
        #     self.early_sign_in = z.total_seconds() / 3600
    # @api.onchange('check_out', 'hour_to')
    # def compute_early_late(self):
    #     if self.check_out:
    #         date_check_out = dt.strptime(str(self.check_out), '%Y-%m-%d %H:%M:%S').time()
    #         planned_check_out = dt(1988, 2, 19, int(self.hour_to))
    #         planned_check_out = planned_check_out.strftime('%H:%M:%S')
    #         date_hour_to = dt.strptime(str(planned_check_out), '%H:%M:%S').time()
    #         if date_hour_to < date_check_out:
    #             z = dt.combine(date.today(), date_check_out) - dt.combine(date.today(), date_hour_to)
    #             self.over_time = z.total_seconds() / 3600
    #         elif date_hour_to > date_check_out:
    #             z = dt.combine(date.today(), date_hour_to) - dt.combine(date.today(), date_check_out)
    #             self.early_leave = z.total_seconds() / 3600
