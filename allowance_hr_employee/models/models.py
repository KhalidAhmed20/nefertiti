# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrContract(models.Model):
    _inherit = 'hr.contract'

    # for allowance
    hra = fields.Float(string='Housing Allowance')
    tr_allowance = fields.Float(string='Transportation Allowance ')
    risk_allowance = fields.Float(string='Risks Allowance')
    food_allowance = fields.Float(string='Food Allowance')
    attendence_allowance = fields.Selection([('a_100', '100'), ('a_300', '300')], string="Attendence Allowance")
    a_100_300 = fields.Integer(compute='func_100_300')

    # for deduction
    ## for fellowship funds
    applied_fellow = fields.Boolean(string="Apply On Fellowship Funds", default=True)
    fellow_type = fields.Selection([('percentage', 'Percentage'), ('amount', 'Amount')], string="Type")
    fellow_percentage = fields.Float(string="Percentage")
    fellow_amount = fields.Float(String="Amount")
    ## for social insurance
    applied_social = fields.Boolean(string="Apply On Social Insurance", default=True)
    insurance_salary = fields.Float(string="Insurance Salary")
    company_insurance_rate = fields.Float(string="Company Insurance Rate", compute='_compute_insurance_amount')
    company_insurance_value = fields.Float(string="Company Insurance Value", compute='_compute_insurance_amount')
    insurance_amount = fields.Float(string="Insurance Amount", compute='_compute_insurance_amount')
    insurance_date = fields.Date(string="Insurance Date")
    insurance_number = fields.Char(string="Insurance No")
    insurance_job_desc = fields.Char(string="Insurance Job DESC")
    social_reject_reason = fields.Text(string="Reason For Non Registration")
    ##for medical Care
    applied_medical_emp = fields.Boolean(string="Apply On Medical Care (Employee)", default=True)
    applied_medical_fam = fields.Boolean(string="Apply On Medical Care (Family)", default=False)
    medical_class = fields.Selection([('a', 'A'), ('b', 'B'), ('c', 'C')], string="Class")
    coverage_rate = fields.Float(string="Coverage Rate %")
    medical_emp_amount = fields.Float(string="Employee Amount")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    medical_fam_amount = fields.Float(string="Family Amount")
    medical_fam_ids = fields.One2many('medical.employee.family', 'contract_emp_id')
    ## for medical insurance
    applied_medical_insurance = fields.Boolean(string="Apply On Medical Insurance", default=True)
    med_insur_card_no = fields.Char(string="Card No")
    med_insur_issue_date = fields.Date(string="Issue Date")
    med_insur_end_date = fields.Date(string="End Date")
    applied_111_app = fields.Boolean(string="Apply On 111 APP")

    # @api.depends('insurance_salary')
    # def get_company_insurance_rale(self):
    #     for rec in self:
    #         rec.company_insurance_rale = rec.company_insurance_rale
    #         rec.company_insurance_rate = 18.57
    #         rec.company_insurance_rale = rec.company_insurance_rate * rec.insurance_salary

    @api.onchange('fellow_percentage')
    def compute_fellow_amount_depend_on_percentage(self):
        if self.fellow_percentage:
            self.fellow_amount = (self.fellow_percentage * self.wage) / 100

    @api.depends('attendence_allowance')
    def func_100_300(self):
        for rec in self:
            if rec.attendence_allowance == 'a_100':
                print("100")
                rec.a_100_300 = 100
            elif rec.attendence_allowance == 'a_300':
                print("300")
                rec.a_100_300 = 300
            else:
                print("00")
                rec.a_100_300 = 0

    @api.depends('insurance_salary')
    def _compute_insurance_amount(self):
        for rec in self:
            rec.insurance_amount = rec.insurance_salary * .11
            rec.company_insurance_rate = 18.75
            rec.company_insurance_value = rec.insurance_salary * (rec.company_insurance_rate / 100)


class MedicalEmployeeFamily(models.Model):
    """Table for employee family Medical insurance info"""

    _name = 'medical.employee.family'
    _description = 'Medical Employee Family'

    contract_emp_id = fields.Many2one('hr.contract')
    member_name = fields.Char(string='Name')
    relation_id = fields.Many2one('hr.employee.relation', string="Relation", help="Relationship with the employee")
    medical_class = fields.Selection([('a', 'A'), ('b', 'B'), ('c', 'C')], string="Class")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")




