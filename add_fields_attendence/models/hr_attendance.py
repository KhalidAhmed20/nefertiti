from odoo import api, fields, models


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    emp_code = fields.Char('Employee Code', related='employee_id.emp_code')
