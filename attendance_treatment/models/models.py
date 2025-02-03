# -*- coding: utf-8 -*-

import datetime
from odoo import models, fields, api
from datetime import datetime as dt, date, timedelta
from dateutil.relativedelta import relativedelta


class AttendanceTreatment(models.Model):
    _name = 'attendance.treatment'
    _description = 'hr attendance treatment'

    employee_id = fields.Many2one('hr.employee', string="Employee Name")
    check_in = fields.Datetime(string="Check In")
    check_out = fields.Datetime(string="Check Out")
    from_date = fields.Date()
    to_date = fields.Date()



    @api.model
    def create(self, vals_list):
        res=super(AttendanceTreatment, self).create(vals_list)
        res.get_data()
        return res

    def get_data(self):
        for rec in self:
            rec.from_date=rec.check_in.date()
            rec.to_date=rec.check_in.date()


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    @api.constrains('check_in', 'check_out', 'employee_id')
    def _check_validity(self):
        return True


