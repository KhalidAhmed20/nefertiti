# -*- coding: utf-8 -*-

from odoo import models, fields, api
import random
import datetime
from datetime import datetime, timedelta, date


class EditHrAttendance(models.Model):
    _inherit = 'hr.attendance'

    hr_attend = fields.Many2one(comodel_name="hr.payslip", string="", required=False, )


class HrPayrollStructureInherit(models.Model):
    _inherit = 'hr.payroll.structure'

    struct_number = fields.Integer(string="Struct Number", required=False, )


class EditHrPayslip(models.Model):
    _inherit = 'hr.payslip'

    # struct_number = fields.Integer(string="Struct Number", required=False, )
    emp_code = fields.Char(String="Emp Code", related="employee_id.emp_code")
    work_location = fields.Many2one(related='employee_id.work_location_id', readonly=False, related_sudo=False)
    equipment = fields.Char(related='employee_id.equipment', readonly=False, related_sudo=False)
    hr_attend_ids = fields.One2many(comodel_name="hr.attendance", inverse_name="hr_attend", string="",
                                    required=False, compute="get_hr_attend_ids")
    total_actual_hours = fields.Float(string="Total Actual Hours", required=False, compute='get_total_actual_hours')
    shift_name_ids = fields.One2many(comodel_name="employee.shift.line", inverse_name="shift_payroll_id",
                                     string="", required=False, compute="get_hr_attend_ids")
    fridays_payroll_ids = fields.One2many(comodel_name="employee.fridays.line", inverse_name="fridays_payroll_id",
                                          string="", required=False, compute="get_fridays_ids")
    rest_payroll_ids = fields.One2many(comodel_name="employee.rest.line", inverse_name="rest_payroll_id",
                                       string="", required=False, compute="get_rest_ids")
    overtime_payrol_ids = fields.One2many(comodel_name="hr.overtime", inverse_name="overtime_payrol_id", string="",
                                          required=False, compute="get_overtime_payrol_ids")
    address_id = fields.Many2one(
        'res.partner',
        string='Work Address',
        compute="_compute_address_id",
        precompute=True,
        store=True,
        readonly=False,
        check_company=True)

    @api.depends('company_id')
    def _compute_address_id(self):
        for employee in self:
            address = employee.company_id.partner_id.address_get(['default'])
            employee.address_id = address['default'] if address else False
    # overtime
    @api.depends('employee_id', 'date_from', 'date_to', )
    def get_overtime_payrol_ids(self):
        for rec in self:
            overtime_payr = rec.env['hr.overtime'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('date_to', '<=', rec.date_to),
                ('date_from', '>=', rec.date_from),
                ('state', '=', 'approved'),
            ])
            if overtime_payr:
                rec.overtime_payrol_ids = overtime_payr
            else:
                rec.overtime_payrol_ids = False

    # Fridays
    @api.depends('employee_id', 'date_from', 'date_to', )
    def get_fridays_ids(self):
        for rec in self:
            fridays = rec.env['hr.employee'].sudo().search([
                ('id', '=', rec.employee_id.id),
                ('fridays_ids', '!=', False),
            ], limit=1)
            list = []
            if fridays:
                for friday in fridays.fridays_ids:
                    if friday.date_from >= rec.date_from and friday.date_to <= rec.date_to:
                        list.append(friday.id)
                    else:
                        rec.fridays_payroll_ids = rec.fridays_payroll_ids
                rec.fridays_payroll_ids = list
            else:
                rec.fridays_payroll_ids = False

    # The Rest
    @api.depends('employee_id', 'date_from', 'date_to', )
    def get_rest_ids(self):
        for rec in self:
            rests = rec.env['hr.employee'].search([
                ('id', '=', rec.employee_id.id),
                ('the_rest_ids', '!=', False),
            ], limit=1)
            list = []
            if rests:
                for rest in rests.the_rest_ids:
                    if rest.date_from >= rec.date_from and rest.date_to <= rec.date_to:
                        list.append(rest.id)
                    else:
                        rec.rest_payroll_ids = rec.rest_payroll_ids
                rec.rest_payroll_ids = list
            else:
                rec.rest_payroll_ids = False

    # attendance and shift attendance
    @api.depends('employee_id', 'date_from', 'date_to', )
    def get_total_actual_hours(self):
        for rec in self:
            rec.total_actual_hours = 0
            tot = 0
            if rec.hr_attend_ids:
                for attend in rec.hr_attend_ids:
                    tot += attend.actual_worked_hours
            rec.total_actual_hours = tot

    # attendance and shift attendance
    @api.depends('employee_id', 'date_from', 'date_to', )
    def get_hr_attend_ids(self):
        for rec in self:
            shift_attend = rec.env['hr.employee'].search([
                ('id', '=', rec.employee_id.id),
                ('shift_name_ids', '!=', False),
            ])
            attend = rec.env['hr.attendance'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('check_in', '<=', rec.date_to),
                ('check_in', '>=', rec.date_from),
            ])
            if attend:
                rec.hr_attend_ids = attend
            else:
                rec.hr_attend_ids = False
            if shift_attend:
                rec.shift_name_ids = shift_attend.shift_name_ids
            else:
                rec.shift_name_ids = False

    # calculation fields

    rate = fields.Float(string="rate", required=False, readonly=True, default="0.5")
    net_late_hours = fields.Float(string="net_late_hours", required=False, )
    month_days = fields.Float(string="Month Days", compute="get_calculation")  # Day
    frist_time = fields.Float(string="frist_time", compute="get_days")  # Day
    second_time = fields.Float(string="second_time", compute="get_days")  # Day
    third_time = fields.Float(string="third_time", compute="get_days")  # Day
    fourth_time = fields.Float(string="fourth_time", compute="get_days")  # Day
    fifth_time = fields.Float(string="fifth_time", compute="get_days")  # Day
    attendance_days = fields.Float(string="Attendance Days")  # code=100
    finger_print_attendance_days = fields.Float(string="Finger Attendance Days", compute="get_calculation")
    total_late_hours = fields.Float(string="Total Late Hours", )
    total_sign_out_hours = fields.Float(string="Total SignOut Hours", )
    absence_without_permission = fields.Float(string="Absence Without Permission", compute="get_calculation")
    total_penalties = fields.Float(string="Total Penalties", required=False, compute="get_days_penalties")
    total_penalties_edit = fields.Float(string="Total Penalties", required=False, readonly=True)
    total_deduction = fields.Float(string="Total Deduction", required=False, compute="get_days_penalties")
    total_deduction_edit = fields.Float(string="Total Deduction Edit", required=False, compute="get_days_penalties")
    over_days = fields.Float(string="Over Days", )
    compute_late_hours = fields.Float(string="Compute Late Hours", )
    compute_sign_out_hours = fields.Float(string="Compute SignOut Hours", )
    net_sign_out_hours = fields.Float(string="Net SignOut Hours", )
    net_late_hours = fields.Float(string="Net Late Hours", )
    total_late_signout_permission = fields.Float(string="Total Late Signout Permission", )
    permit_4 = fields.Float(string="Permitted 4", default=4)
    diff_4 = fields.Float(stringe="Difference", )
    # اضافي الساعات بنظام الساعة و نصف والساعتين
    hour_15_bonus = fields.Float()
    hour_2_bonus = fields.Float()
    # حساب حافز الانتظام
    a_100 = fields.Float()
    a_300 = fields.Float()

    rest_allowance = fields.Float(string="Rest Allowance")  # code=103
    rest_discount = fields.Float(string="Rest Allowance", compute="get_rest_allowance")  # code=103
    hours_mission = fields.Float(string="Hours Mission")  # code=116
    late_permission = fields.Float(string="Late Permission")  # code=105
    early_sign_out = fields.Float(string="Early Sign Out")  # code=106
    casual_leave = fields.Float(string="casual Leave")  # code=109
    casual_leave2022 = fields.Float(string="casual Leave 2022")  # code=109
    general_leave = fields.Float(string="general leave")  # code=110
    general_leave2022 = fields.Float(string="general leave 2022")  # code=110
    absence_with_permission = fields.Float(string="Absence With Permission")
    paid_leave = fields.Float(string="paid leave")  # code=111
    car_late_permission = fields.Float(string="Car Late Permission")  # code=118
    # freelancing field
    freelancing_days = fields.Float(string="Freelancing Working Days")
    # no of fridays
    fridays_no = fields.Integer(string="Fridays")
    extra_daily_n = fields.Float(string="extra_daily_n", required=False, compute="get_calculation")
    extra_night_n = fields.Float(string="extra_night_n", required=False, compute="get_calculation")
    extra_daily = fields.Float(string="extra_daily", required=False, compute="get_calculation")
    extra_dailys = fields.Float(string="extra_dailys", required=False, compute="get_calculation")
    extra_night = fields.Float(string="extra_night", required=False, compute="get_calculation")
    implement_daily = fields.Float(string="implement_daily", required=False, compute="get_calculation")
    implement_night = fields.Float(string="implement_night", required=False, compute="get_calculation")

    @api.depends('employee_id', 'date_from', 'date_to', )
    def get_calculation(self):
        for rec in self:
            rec.finger_print_attendance_days = rec.fridays_no = rec.rest_allowance = rec.month_days = extra_daily_n = extra_night_n = extra_daily = extra_dailys = extra_night = implement_daily = implement_night = 0
            casual_leave = 0
            casual_leave2022 = 0
            general_leave = 0
            general_leave2022 = 0
            absence_with_permission = 0
            paid_leave = 0
            late_permission = 0
            hours_mission = 0
            car_late_permission = 0
            early_sign_out = 0
            if rec.employee_id and rec.date_from and rec.date_to:
                rec.month_days = (rec.date_to - rec.date_from).days + 1
                rec.finger_print_attendance_days = len(rec.hr_attend_ids.ids)
                rec.fridays_no = len(rec.fridays_payroll_ids.ids)
                rec.rest_allowance = len(rec.rest_payroll_ids.ids)
                for overtime_in_attendance in rec.hr_attend_ids:
                    if overtime_in_attendance.is_day_shift == "day":
                        extra_daily_n += overtime_in_attendance.net_over_time
                    if overtime_in_attendance.is_day_shift == "night":
                        extra_night_n += overtime_in_attendance.net_over_time
                for overtime in rec.overtime_payrol_ids:
                    if overtime.hour_type_bonus == 'b_5':
                        extra_daily += overtime.over_hours
                    elif overtime.hour_type_bonus == 'b_6':
                        extra_night += overtime.over_hours
                    elif overtime.hour_type_bonus == 'b_7':
                        implement_daily += overtime.over_hours
                    elif overtime.hour_type_bonus == 'b_8':
                        implement_night += overtime.over_hours
                    elif overtime.hour_type_bonus == 'b_9':
                        extra_dailys += overtime.over_hours
                rec.extra_daily_n, rec.extra_night_n, rec.extra_daily, rec.extra_dailys, rec.extra_night, rec.implement_daily, rec.implement_night = extra_daily_n, extra_night_n, extra_daily, extra_dailys, extra_night, implement_daily, implement_night
                time_offs = self.env['hr.leave'].search(
                    [('state', '=', 'validate'), ('employee_id', '=', rec.employee_id.id),
                     ('request_date_to', '<=', self.date_to), ('request_date_from', '>=', self.date_from), ])
                for offe in time_offs:
                    print('offe.holiday_status_id.id', offe.holiday_status_id.id)
                    if offe.holiday_status_id.id == self.env.ref('payrol_add_attendance.id_casual_leave').id:
                        casual_leave += offe.number_of_days
                    elif offe.holiday_status_id.id == 22:
                        general_leave += offe.number_of_days
                    elif offe.holiday_status_id.id == self.env.ref('__export__.hr_leave_type_33_7352cd31').id:
                        casual_leave2022 += offe.number_of_days
                    elif offe.holiday_status_id.id == self.env.ref('__export__.hr_leave_type_32_3b52e0ba').id:
                        general_leave2022 += offe.number_of_days
                    elif offe.holiday_status_id.id == 29:
                        absence_with_permission += offe.number_of_days
                    elif offe.holiday_status_id.id == self.env.ref('payrol_add_attendance.id_paid_leave').id:
                        paid_leave += offe.number_of_days
                    elif offe.holiday_status_id.id == self.env.ref('payrol_add_attendance.id_late_permission').id:
                        if offe.request_unit_hours == True:
                            late_permission += offe.duration_hour
                        else:
                            late_permission += offe.number_of_hours_display
                    elif offe.holiday_status_id.id == self.env.ref('payrol_add_attendance.id_hours_mission').id:
                        if offe.request_unit_hours == True:
                            hours_mission += offe.duration_hour
                        else:
                            hours_mission += offe.number_of_hours_display
                    elif offe.holiday_status_id.id == self.env.ref('payrol_add_attendance.id_car_late_permission').id:
                        if offe.request_unit_hours == True:
                            car_late_permission += offe.duration_hour
                        else:
                            car_late_permission += offe.number_of_hours_display
                    elif offe.holiday_status_id.id == self.env.ref('payrol_add_attendance.id_early_sign_out').id:
                        if offe.request_unit_hours == True:
                            early_sign_out += offe.duration_hour
                        else:
                            early_sign_out += offe.number_of_hours_display
                rec.casual_leave = casual_leave
                rec.casual_leave2022 = casual_leave2022
                rec.general_leave = general_leave
                rec.general_leave2022 = general_leave2022
                rec.absence_with_permission = absence_with_permission
                rec.paid_leave = paid_leave
                rec.late_permission = late_permission
                rec.hours_mission = hours_mission
                rec.car_late_permission = car_late_permission
                rec.early_sign_out = early_sign_out
                rec.absence_without_permission = rec.month_days - rec.finger_print_attendance_days - rec.fridays_no - rec.casual_leave - rec.casual_leave2022 - rec.general_leave2022 - rec.general_leave - rec.absence_with_permission - rec.rest_allowance - rec.paid_leave
                late = 0
                early_leave = 0
                for attend in rec.hr_attend_ids:
                    if attend.late > .25:
                        late += attend.late
                    if attend.early_leave > .25:
                        early_leave += attend.early_leave
                rec.total_late_hours = late
                rec.total_sign_out_hours = early_leave
                rec.compute_sign_out_hours = early_leave - rec.early_sign_out
                rec.compute_late_hours = late - rec.late_permission - rec.hours_mission - rec.car_late_permission
                rec.net_late_hours = rec.compute_late_hours * rec.rate
                rec.net_sign_out_hours = rec.compute_sign_out_hours * rec.rate
            else:
                rec.absence_without_permission, rec.early_sign_out, rec.car_late_permission, rec.hours_mission, rec.late_permission, rec.paid_leave, rec.rest_allowance, rec.general_leave, rec.general_leave2022, rec.absence_with_permission, rec.casual_leave, rec.casual_leave2022, rec.extra_daily_n, rec.extra_night_n, rec.extra_daily, rec.extra_dailys, rec.extra_night, rec.implement_daily, rec.implement_night = rec.absence_without_permission, rec.early_sign_out, rec.car_late_permission, rec.hours_mission, rec.late_permission, rec.paid_leave, rec.rest_allowance, rec.general_leave, rec.general_leave2022, rec.absence_with_permission, rec.casual_leave, rec.casual_leave2022, rec.extra_daily_n, rec.extra_night_n, rec.extra_daily, rec.extra_dailys, rec.extra_night, rec.implement_daily, rec.implement_night

    @api.depends('absence_without_permission')
    def get_days(self):
        if self.absence_without_permission:
            for rec in self:
                rec.frist_time = 0
                rec.third_time = 0
                rec.second_time = 0
                rec.fourth_time = 0
                rec.fifth_time = 0
                if rec.absence_without_permission >= 1:
                    rec.frist_time = 1
                if rec.absence_without_permission >= 2:
                    rec.second_time = 1.5
                if rec.absence_without_permission >= 3:
                    rec.third_time = 2
                if rec.absence_without_permission >= 4:
                    rec.fourth_time = 3
                if rec.absence_without_permission >= 5:
                    rec.fifth_time = 4
        else:
            for rec in self:
                rec.frist_time = 0
                rec.third_time = 0
                rec.second_time = 0
                rec.fourth_time = 0
                rec.fifth_time = 0

    # get days penalties
    @api.depends('employee_id', 'date_from', 'date_to')
    def get_days_penalties(self):
        for rec in self:
            rec.total_deduction_edit = rec.total_deduction_edit
            days_penalties = sum(rec.env['penalities'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('state', '=', 'confirmed'),
                ('date', '<=', rec.date_to),
                ('date', '>=', rec.date_from),
            ]).mapped('days'))
            rec.total_penalties = days_penalties
            if rec.frist_time or rec.second_time or rec.third_time or rec.fourth_time \
                    or rec.fifth_time or rec.total_penalties or rec.absence_without_permission:
                rec.total_deduction = rec.frist_time + rec.second_time + rec.third_time + rec.fourth_time + \
                                       rec.fifth_time + rec.total_penalties + rec.absence_without_permission
                rec.total_penalties_edit = rec.frist_time + rec.second_time + rec.third_time + rec.fourth_time + \
                                            rec.fifth_time
                rec.total_deduction_edit = rec.total_penalties + rec.total_penalties_edit
            else:
                rec.total_deduction = False
        # if self.total_deduction < 6:
        # else:
        #     self.total_deduction_edit = 5

    @api.depends('employee_id', 'date_from', 'date_to', )
    def get_rest_allowance(self):
        for rec in self:
            the_coefficient = self.env['hr.employee'].search([
                ('id', '=', self.employee_id.id), ])
            rec.rest_discount = (rec.rest_allowance * rec.struct_id.struct_number) * (
                the_coefficient.the_coefficient) - (rec.rest_allowance * rec.struct_id.struct_number)


# inherit over time


class EditHrOvertime(models.Model):
    _inherit = 'hr.overtime'

    overtime_payrol_id = fields.Many2one(comodel_name="hr.payslip", string="", required=False, )

