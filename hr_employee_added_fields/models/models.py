# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime
from datetime import date


class HrEmployeePrivate(models.Model):

    _inherit = 'hr.employee'

    emp_code = fields.Char(String="Emp Code")
    _sql_constraints = [
        ('emp_code_uniq', 'unique (emp_code)',
         'this emp_code is already exist '),
    ]
    # for address center and governorate
    street = fields.Char(string="Address")
    city = fields.Char(string="city")
    state_id = fields.Many2one('res.country.state', string="State")
    zip = fields.Char(string="ZIP")
    country_id = fields.Many2one('res.country')

    age = fields.Char('Age', compute='compute_age')

    religion = fields.Selection([
        ('muslim', 'مسلم'),
        ('christian', 'مسيحي'),
        ('other', 'أخري')
    ], groups="hr.group_hr_user", string="Religion")
    military_state = fields.Selection([
        ('1', 'أجنبي'),
        ('2', 'أدي الخدمة'),
        ('3', 'أنهى الخدمة'),
        ('4', 'تحت الطلب'),
        ('5', 'طالب'),
        ('6', 'لم يبلغ سن الالتزام'),
        ('7', 'متخلف'),
        ('8', 'معفى'),
        ('9', 'معفى مؤقت'),
    ], groups="hr.group_hr_user", string="Military State")

#     driving info
    driving_licence = fields.Char(string="Driving Licence")
    driving_licence_type = fields.Selection([
        ('private', 'خاصة'),
        ('international', 'دولية'),
        ('first', 'أولي'),
        ('second', 'ثانية'),
        ('third', 'ثالثة')
    ], groups="hr.group_hr_user", string="Type")
    driving_licence_extract = fields.Char(string="Extraction Place")
    job_grade = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
    ], groups="hr.group_hr_user", string="Job Grade")
    certification_id = fields.Many2one('certification.level', string="Certification")

    @api.depends('birthday')
    def compute_age(self):
        for rec in self:
            if rec.birthday:
                dt = rec.birthday
                d1 = datetime.strptime(str(dt), "%Y-%m-%d").date()
                d2 = date.today()
                rd = relativedelta(d2, d1)
                rec.age = str(rd.years) + ' years'
                print(str(rd.years) + ' years')
            else:
                rec.age = '0'


class Certificate(models.Model):
    _name = "certification.level"

    name = fields.Char(string="certificate Name")


