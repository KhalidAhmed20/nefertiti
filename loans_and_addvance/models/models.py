# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timedelta
from num2words import num2words


class LoansAndAddvance(models.Model):
    _name = 'loans'
    _description = 'loans_Description'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    @api.model
    def get_journal(self):
        journal = self.env['account.journal'].sudo().search([('is_loan', '=', True)], limit=1).id
        return journal

    state = fields.Selection([("draft", "Draft"), ("validate", "Validate"), ("confirmed", "Confirm")], readonly=True,
                             default="draft",
                             tracking=True)
    name = fields.Char('', readonly=True, copy=False, default='New', tracking=True)
    date = fields.Date("Date", tracking=True, required=True)
    deduction_date = fields.Date("Deduction Date", tracking=True, required=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', string="Employee", required=True, tracking=True)
    amount = fields.Float(string="Amount", tracking=True, required=True)
    no_of_installment = fields.Integer(string="No Of Installment", tracking=True, default=1)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department",
                                    related='employee_id.department_id')
    loans_ids = fields.One2many('loans.line', 'loans_id', string="", readonly=True)
    # reason = fields.Text(string="Reason", tracking=True)
    journal_id = fields.Many2one('account.journal', string='Journal', default=get_journal)
    account_id = fields.Many2one('account.account', string='Debit Account', compute='git_account_id_idd')
    account_idd = fields.Many2one('account.account', string='Credit Account', compute='git_account_id_idd')
    loan_id = fields.Many2one('hr.payslip', string='')
    journal_entry_id = fields.Many2one('account.move', string='', copy=False, readonly=True)
    equipment = fields.Char(related='employee_id.equipment', readonly=False, related_sudo=False)
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 readonly=True,
                                 default=lambda self: self.env.company)

    currency_id = fields.Many2one('res.currency', 'Currency', related='company_id.currency_id', readonly=True,
                                  required=True)
    text_amount = fields.Char(string="التفقيط", required=False, compute="amount_to_words_payment", )

    @api.depends('amount')
    def amount_to_words_payment(self):
        for rec in self:
            if rec.company_id.text_amount_language_currency:
                rec.text_amount = rec._l10n_pe_edi_amount_to_text()
            else:
                rec.text_amount = rec.text_amount

    @api.model
    def _l10n_pe_edi_amount_to_text(self):
        """Transform a float amount to text words on peruvian format: AMOUNT IN TEXT 11/100
        :returns: Amount transformed to words peruvian format for invoices
        :rtype: str
        """
        self.ensure_one()
        amount_i, amount_d = divmod(self.amount, 1)
        a = self.company_id.text_amount_language_currency
        words = num2words(amount_i, lang=a)
        if a == "ar":
            words = words.replace('،', ' و')
        elif a == "en":
            words = words.replace(',', ' and')
        result = words + ' ' + self.currency_id.currency_unit_label
        return result

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('loans.loane') or 'New'
        result = super(LoansAndAddvance, self).create(vals)
        return result

    @api.depends('journal_id')
    def git_account_id_idd(self):
        for rec in self:
            rec.account_id = False
            rec.account_idd = False
            if rec.journal_id.account_ids and rec.journal_id.account_idd:
                print('rec.journal_id.account_ids.id', rec.journal_id.account_ids.id)
                rec.account_id = rec.journal_id.account_ids.id
                rec.account_idd = rec.journal_id.account_idd.id
            else:
                print("yyyyyyyyyyyyyyyyyyy")
                rec.account_id = False
                rec.account_idd = False

    def compute_installment(self):
        for rec in self:
            loan_line = []
            no_install = rec.no_of_installment
            rec.loans_ids = False
            date_date = rec.deduction_date
            for line in range(no_install):
                loan_line.append((0, 0, {
                    'name': date_date,
                    'amount': rec.amount / rec.no_of_installment,
                }))
                date_date = date_date + relativedelta(months=1)
                print("date_date", date_date)
            rec.loans_ids = loan_line

    def validate_action(self):
        for rec in self:
            rec.state = 'validate'
    def cancel_action(self):
        for rec in self:
            rec.state = 'draft'
            rec.journal_entry_id.state = 'draft'
            print(rec.journal_entry_id.id)
            print(rec.journal_entry_id.state)


    def confirm_action(self):
        for rec in self:
            invoice = self.env['account.move'].sudo().create({
                'type': 'entry',
                'ref': rec.name,
                'date': rec.date,
                'journal_id': self.journal_id.id,
                'line_ids': [(0, 0, {
                    'account_id': rec.account_id.id,
                    # 'partner_id': rec.employee_id.id,
                    # 'name': rec.employee_id.name,
                    'debit': rec.amount,
                }), (0, 0, {
                    'account_id': rec.account_idd.id,
                    # 'partner_id': rec.employee_id.id,
                    # 'name': rec.employee_id.name,
                    'credit': rec.amount,
                })],
            })
            rec.journal_entry_id = invoice.id
            rec.state = 'confirmed'
            invoice.action_post()





# loan model
class LoansAddvanceLine(models.Model):
    _name = 'loans.line'
    _description = 'loans_line'

    name = fields.Date('Payment Date')
    employee_id = fields.Many2one(comodel_name='hr.employee', string="Employee", related='loans_id.employee_id',
                                  store=True)
    amount = fields.Float('Amount')
    loans_id = fields.Many2one('loans', string='')
    loans_payslip_id = fields.Many2one('hr.payslip', string='')


# salary advance model
class EditSalaryAdvance(models.Model):
    _name = 'salary.advance'
    _description = 'salary advance Description'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    @api.model
    def get_journal(self):
        journal = self.env['account.journal'].sudo().search([('is_salary_advance', '=', True)], limit=1).id
        return journal

    state = fields.Selection([("draft", "Draft"), ("validate", "Validate"), ("confirmed", "Confirm")], readonly=True,
                             default="draft",
                             tracking=True)
    name = fields.Char('', readonly=True, copy=False, default='New', tracking=True)
    date = fields.Date("Date", tracking=True, required=True)
    deduction_date = fields.Date("Deduction Date", tracking=True, required=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', string="Employee", required=True, tracking=True)
    amount = fields.Float(string="Amount", tracking=True, required=True)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department",
                                    related='employee_id.department_id')
    journal_id = fields.Many2one('account.journal', string='Journal', default=get_journal)
    account_id = fields.Many2one('account.account', string='Debit Account', compute='git_account_id_idd')
    account_idd = fields.Many2one('account.account', string='Credit Account', compute='git_account_id_idd')
    reason = fields.Text(string="Reason", tracking=True)
    salary_advance_id = fields.Many2one('hr.payslip', string='')
    journal_entry_id = fields.Many2one('account.move', string='', copy=False, readonly=True)
    equipment = fields.Char(related='employee_id.equipment', readonly=False, related_sudo=False)

    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 readonly=True,
                                 default=lambda self: self.env.company)

    currency_id = fields.Many2one('res.currency', 'Currency', related='company_id.currency_id', readonly=True,
                                  required=True)
    text_amount = fields.Char(string="التفقيط", required=False, compute="amount_to_words_payment", )

    @api.depends('amount')
    def amount_to_words_payment(self):
        for rec in self:
            if rec.company_id.text_amount_language_currency:
                rec.text_amount = rec._l10n_pe_edi_amount_to_text()
            else:
                rec.text_amount = rec.text_amount

    @api.model
    def _l10n_pe_edi_amount_to_text(self):
        """Transform a float amount to text words on peruvian format: AMOUNT IN TEXT 11/100
        :returns: Amount transformed to words peruvian format for invoices
        :rtype: str
        """
        self.ensure_one()
        amount_i, amount_d = divmod(self.amount, 1)
        a = self.company_id.text_amount_language_currency
        words = num2words(amount_i, lang=a)
        if a == "ar":
            words = words.replace('،', ' و')
        elif a == "en":
            words = words.replace(',', ' and')
        result = words + ' ' + self.currency_id.currency_unit_label
        return result

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('salary.advance') or 'New'
        result = super(EditSalaryAdvance, self).create(vals)
        return result

    @api.depends('journal_id')
    def git_account_id_idd(self):
        for rec in self:
            rec.account_id = False
            rec.account_idd = False
            if rec.journal_id.account_ids and rec.journal_id.account_idd:
                print('rec.journal_id.account_ids.id', rec.journal_id.account_ids.id)
                rec.account_id = rec.journal_id.account_ids.id
                rec.account_idd = rec.journal_id.account_idd.id
            else:
                print("yyyyyyyyyyyyyyyyyyy")
                rec.account_id = False
                rec.account_idd = False

    def validate_action(self):
        for rec in self:
            rec.state = 'validate'

    def confirm_action(self):
        for rec in self:
            invoice = self.env['account.move'].sudo().create({
                'type': 'entry',
                'date': rec.date,
                'ref': rec.name,
                'journal_id': self.journal_id.id,
                'line_ids': [(0, 0, {
                    'account_id': rec.account_id.id,
                    # 'partner_id': rec.employee_id.id,
                    # 'name': rec.employee_id.name,
                    'debit': rec.amount,
                }), (0, 0, {
                    'account_id': rec.account_idd.id,
                    # 'partner_id': rec.employee_id.id,
                    # 'name': rec.employee_id.name,
                    'credit': rec.amount,
                })],
            })
            rec.journal_entry_id = invoice.id
            invoice.action_post()
            rec.state = 'confirmed'




class HrPaysLipInherit(models.Model):
    _inherit = 'hr.payslip'

    # loan_ids = fields.One2many(comodel_name="loans", inverse_name="loan_id", string="", required=False,
    #                            compute='get_loan_ids')
    loans_line_ids = fields.One2many(comodel_name="loans.line", inverse_name="loans_payslip_id", string="",
                                     required=False,
                                     compute='get_loan_ids')
    loans = fields.Float(string="Loans", compute='get_total_loans', )
    salary_advance_ids = fields.One2many(comodel_name="salary.advance", inverse_name="salary_advance_id", string="",
                                         required=False, compute='get_salary_advance_ids')
    salary_advance = fields.Float(string="Salary Advance", compute='get_total_salary_advance', )

    @api.depends('employee_id', 'date_from', 'date_to', )
    def get_loan_ids(self):
        for rec in self:
            rec.loans_line_ids = False
            loans = self.env['loans'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('state', '=', 'confirmed'),
                # ('deduction_date', '<=', self.date_to),
                # ('deduction_date', '>=', self.date_from),
                ('loans_ids', '!=', False),
            ])
            list = []
            if loans:
                for loan in loans.loans_ids:
                    if loan.name >= rec.date_from and loan.name <= rec.date_to:
                        list.append(loan.id)
                rec.loans_line_ids = list
            else:
                rec.loans_line_ids = False

    @api.depends('employee_id', 'date_from', 'date_to', )
    def get_salary_advance_ids(self):
        for rec in self:
            rec.salary_advance_ids = False
            salary_advance = self.env['salary.advance'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('state', '=', 'confirmed'),
                ('deduction_date', '<=', rec.date_to),
                ('deduction_date', '>=', rec.date_from),
            ])
        if salary_advance:
            for rec in self:
                rec.salary_advance_ids = salary_advance
        else:
            self.salary_advance_ids = False

    def calculate_total_loans(self):
        payslips = self.env['hr.payslip'].sudo().search([])
        for payslip in payslips:
            # payslip.loans = False
            # if payslip.loans_line_ids:
            #     for line in payslip.loans_line_ids:
            #         loan_loan = loan_loan + line.amount
            #     rec.loans = loan_loan
            # else:
            #     rec.loans = False
            payslip.get_total_loans()

    def calculate_total_advance(self):
        print('cccccccccccccccccccc')
        payslips = self.env['hr.payslip'].sudo().search([])
        print('payslips', payslips)
        for payslip in payslips:
            advance = 0
            print('payslip', payslip)
            payslip.salary_advance = False
            print('payslip.salary_advance_ids', payslip.salary_advance_ids)
            salary_advance = self.env['salary.advance'].search([
                ('employee_id', '=', payslip.employee_id.id),
                ('state', '=', 'confirmed'),
                ('deduction_date', '<=', payslip.date_to),
                ('deduction_date', '>=', payslip.date_from),
            ])
            if salary_advance:
                for line in salary_advance:
                    advance = advance + line.amount

                payslip.salary_advance = advance
                print('payslip.salary_advance', payslip.salary_advance)
            else:
                payslip.salary_advance = False

    @api.depends('employee_id', 'date_from', 'date_to', )
    def get_total_loans(self):
        loan_loan = 0
        for rec in self:
            rec.loans = False
            if rec.loans_line_ids:
                for line in rec.loans_line_ids:
                    loan_loan = loan_loan + line.amount
                rec.loans = loan_loan
            else:
                rec.loans = False

    @api.depends('employee_id', 'date_from', 'date_to', )
    def get_total_salary_advance(self):
        advance = 0
        for rec in self:
            rec.salary_advance = False
            if rec.salary_advance_ids:
                for line in rec.salary_advance_ids:
                    advance = advance + line.amount
                rec.salary_advance = advance
            else:
                rec.salary_advance = False


#
class AccountJournalInherit(models.Model):
    _inherit = 'account.journal'

    is_loan = fields.Boolean(string="Is Loan", )
    is_salary_advance = fields.Boolean(string="Is Salary Advance", )
    account_ids = fields.Many2one('account.account', string='Debit Account', )
    account_idd = fields.Many2one('account.account', string='Credit Account', )
