# -*- coding: utf-8 -*-

import datetime
from odoo import models, fields, api
from datetime import datetime as dt, date, timedelta
from dateutil.relativedelta import relativedelta


class WizardTreatment(models.Model):
    _name = 'wizard.treatment'
    _description = 'date wizard treatment'

    name = fields.Char(string="Name")
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    is_do_treatment = fields.Boolean(string="",  copy=False)


    def do_treatment_2(self):
        for rec in self:
            employees = self.env['hr.employee'].search([])
            for employe in employees:
                list_ids=[]
                x_from = rec.date_from
                x_to = rec.date_to
                while x_from <= x_to:
                    shift=self.env['employee.shift.line'].sudo().search([('shift_name_id','=',employe.id),('date_from','=',x_from)],limit=1)
                    if shift.hour_from and shift.hour_to:
                        check_in = dt.combine(shift.date_from, datetime.time.min)+relativedelta(hours = shift.hour_from - 4)
                        check_out = dt.combine(shift.date_to, datetime.time.min)+relativedelta(hours = shift.hour_to + 4)
                        day_atts_in = self.env['attendance.treatment'].search([('employee_id', '=', employe.id),('check_in', '>=',check_in),('check_in', '<=',check_out),('id','not in',list_ids)],order='check_in')
                        for id in day_atts_in.ids:
                            list_ids.append(id)
                        if day_atts_in:
                            first_one = day_atts_in[0]
                            last_one = day_atts_in[-1]
                            if len(day_atts_in.ids) == 1:
                                if shift.hour_from - 4 <= day_atts_in[0].check_in.hour + day_atts_in.check_in.minute/60 <= shift.hour_from + 4:
                                    attendance = self.env['hr.attendance'].create({'employee_id': employe.id,'check_in': first_one.check_in,})
                                else:
                                    attendance = self.env['hr.attendance'].create({'employee_id': employe.id,'check_in': first_one.check_in,'check_out': last_one.check_in})
                            else:
                                attendance = self.env['hr.attendance'].create({'employee_id': employe.id,'check_in': first_one.check_in,'check_out': last_one.check_in})
                            if attendance and shift:
                                attendance.date_from = shift.date_from
                                attendance.date_to = shift.date_to
                                attendance.hour_from = shift.hour_from
                                attendance.hour_to = shift.hour_to
                                attendance.is_day_shift = shift.is_day_shift
                                attendance.compute_early_late()
                    else:
                        day_atts_in = self.env['attendance.treatment'].search([('employee_id', '=', employe.id),('check_in', '>=',x_from),('check_in', '<=',x_from),('id','not in',list_ids)],order='check_in')
                        for id in day_atts_in.ids:
                            list_ids.append(id)
                        if day_atts_in:
                            first_one = day_atts_in[0]
                            last_one = day_atts_in[-1]
                            attendance = self.env['hr.attendance'].create(
                                {'employee_id': employe.id, 'check_in': first_one.check_in,
                                 'check_out': last_one.check_in})
                    x_from = x_from + relativedelta(days=1)
                    rec.is_do_treatment=True

