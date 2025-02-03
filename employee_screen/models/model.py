
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from datetime import datetime, timedelta, date


class PurchaseRequestLine(models.Model):
    _name = "penalities"
    _description = "penalities"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    state = fields.Selection([("draft", "Draft"), ("confirmed", "Confirmed")], readonly=True, default="draft",
                             tracking=True)
    name = fields.Text(string="Description", tracking=True)
    date = fields.Date("Date", tracking=True, )
    employee_id = fields.Many2one(comodel_name='hr.employee', string="Employee", required=True, tracking=True)
    payslip_id = fields.Many2one(comodel_name='hr.payslip', string="payslip_id")
    penality_group = fields.Many2one(comodel_name='penality.group', string="Penality Group")
    sub_penality = fields.Many2one(comodel_name='penality.sub', string="Sub Penality"
                                   ,domain="[('penality_group', '=', penality_group)]")
    computation = fields.Selection([("day", "Day"), ("amount", "Amount")], string="Computation", tracking=True)
    days = fields.Float(string="Days", tracking=True)
    # amount = fields.Float(string="Amount", tracking=True)
    type = fields.Selection([("managerial", "Managerial"), ("financial", "Financial")], string="Deduction Type",
                            required=True, tracking=True)
    reason = fields.Text(string="Reason", tracking=True)
    company_id = fields.Many2one(comodel_name='res.company', string="Company", related='employee_id.company_id')
    department_id = fields.Many2one(comodel_name="hr.department", string="Department",
                                    related='employee_id.department_id')
    division = fields.Many2one('hr.department', string="Division", )
    job_id = fields.Many2one('hr.job', 'Job Position', related='employee_id.job_id')
    parent_id = fields.Many2one('hr.employee', 'Manager', related='employee_id.parent_id')
    emp_code = fields.Char(String="Emp Code", )

    # @api.onchange("days")
    # def get_amount_from_contract(self):
    #     print("1111111")
    #     wage_contract = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)], limit=1)
    #     print("222222", wage_contract)
    #     for rec in self:
    #         if wage_contract:
    #             print("33333333", wage_contract.wage)
    #             print("44444444", rec.days)
    #             rec.amount = (wage_contract.wage / 30) * rec.days
    #             print("555555555", rec.amount)

    def git_confirmed(self):
        self.state = "confirmed"


class HrPayslipInherit(models.Model):
    _inherit = 'hr.payslip'

    penalities_ids = fields.One2many(comodel_name="penalities", inverse_name="payslip_id", string="", required=False, )
    penality = fields.Float(string="الجزاءات")

    def back_to_draft(self):
        for rec in self:
            rec.state = 'draft'

    # 'attendence_added_fields'

    @api.onchange('employee_id', 'date_from', 'date_to', )
    def get_penalities_ids(self):
        penality = self.env['penalities'].search([
            ('employee_id', '=', self.employee_id.id),
            ('state', '=', 'confirmed'),
            ('date', '<=', self.date_to),
            ('date', '>=', self.date_from),
        ])
        if penality:
            for rec in self:
                rec.penalities_ids = penality
        else:
            self.penalities_ids = False

    # @api.onchange('employee_id', 'date_from', 'date_to', )
    # def get_penalties(self):
    #     penalit = 0
    #     if self.penalities_ids:
    #         for line in self.penalities_ids:
    #             penalit = penalit + line.amount
    #         self.penality = penalit


class PenalityGroup(models.Model):
    _name = "penality.group"
    _description = "penalities group"

    name = fields.Char(string="Group Name", required=True)


class SubPenality(models.Model):
    _name = "penality.sub"
    _description = "penalities sub"

    name = fields.Char(string="Sub Penality", required=True)
    penality_group = fields.Many2one(comodel_name='penality.group', string="Penality Group", required=True)
