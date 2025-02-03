from odoo import api, fields, models

# It has been added to 17
class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    emp_code = fields.Char(string="Employee Code")



class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    emp_code = fields.Char('Employee Code', related='employee_id.emp_code')
