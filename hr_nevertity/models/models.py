# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class hremployee(models.Model):
    _inherit = 'hr.employee'

    shift_name_ids = fields.One2many(comodel_name="employee.shift.line", inverse_name="shift_name_id",
                                     string="", required=False, )
    fridays_ids = fields.One2many(comodel_name="employee.fridays.line", inverse_name="fridays_id",
                                  string="", required=False, )
    the_rest_ids = fields.One2many(comodel_name="employee.rest.line", inverse_name="the_rest_id",
                                   string="", required=False, )
    the_coefficient = fields.Float(string="The Coefficient", required=False, )
    co_officient_day_overtime = fields.Float(string="Co Officient Day Overtime", required=False, )
    co_officient_night_overtime = fields.Float(string="Co Officient Night Overtime", required=False, )
    rewards = fields.Float(string="Rewards", required=False, )

    def get_fin_product(self):
        return {
            'name': _('Finished Product'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.shift_name_ids.ids)],
            'res_model': 'employee.shift.line',
        }


class EmployeeShiftLine(models.Model):
    _name = 'employee.shift.line'

    name = fields.Char(string="", required=False, )
    shift_name_id = fields.Many2one('hr.employee', string="")
    shift_payroll_id = fields.Many2one('hr.payslip', string="")
    employee_id = fields.Char(string="Employee", related='shift_name_id.name')
    shift_name = fields.Many2one('shift.name', string="Shift Name")
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date TO")
    hour_from = fields.Float(string="Hour From")
    hour_to = fields.Float(string="Hour To")
    # is_day_shift = fields.Boolean(string="Is Day Shift",  default=False)
    is_day_shift = fields.Selection(string="Is Day Shift", selection=[('day', 'Day'), ('night', 'Night'), ],
                                    required=False, )


class EmployeeFridaysLine(models.Model):
    _name = 'employee.fridays.line'

    employee_id = fields.Many2one(comodel_name='hr.employee', string="Employee", )
    fridays_id = fields.Many2one('hr.employee', string="")
    fridays_payroll_id = fields.Many2one('hr.payslip', string="")
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date TO")


class EmployeeRestsLine(models.Model):
    _name = 'employee.rest.line'

    the_rest_id = fields.Many2one('hr.employee', string="")
    employee_id = fields.Many2one(comodel_name='hr.employee', string="Employee", )
    rest_payroll_id = fields.Many2one('hr.payslip', string="")
    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date TO")


class ShiftName(models.Model):
    _name = 'shift.name'

    name = fields.Char(string="Shift Name")
