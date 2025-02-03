# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EditAccountJournal(models.Model):
    _inherit = 'account.journal'

    category_code = fields.Char(string="Code", required=True, default=0)
    # category_code_check = fields.Char(string="Code", required=True, default=0)
    sequencee_in = fields.Integer(string="Sequence In", default=1, )
    sequencee_out = fields.Integer(string="Sequence Out", default=1, )


class EditAccountPayment(models.Model):
    _inherit = 'account.payment'

    # category_code = fields.Char(string="Code", required=True, default=0)
    sequencee = fields.Char(string="Sequence", readonly=True, default=0, copy=False)
    sequence_douple = fields.Char(string="Sequence", readonly=True, default=0, copy=False)


    @api.onchange('journal_id', 'payment_type', 'destination_journal_id')
    def sequence_code(self):
        for rec in self:
            if rec.journal_id:
                if rec.payment_type == 'inbound':
                    rec.sequencee = rec.journal_id.category_code + '.IN/' + (
                            3 - len(str(rec.journal_id.sequencee_in))) * '0' + str(
                        rec.journal_id.sequencee_in)
                elif rec.payment_type == 'outbound':
                    rec.sequencee = rec.journal_id.category_code + '.OUT/' + (
                            3 - len(str(rec.journal_id.sequencee_out))) * '0' + str(
                        rec.journal_id.sequencee_out)
                elif rec.payment_type == 'transfer':
                    rec.sequencee = rec.journal_id.category_code + '.OUT/' + (
                            3 - len(str(rec.journal_id.sequencee_out))) * '0' + str(
                        rec.journal_id.sequencee_out)
                    if rec.destination_journal_id:
                        rec.sequence_douple = rec.destination_journal_id.category_code + '.In/' + (
                                3 - len(str(rec.destination_journal_id.sequencee_in))) * '0' + str(
                            rec.destination_journal_id.sequencee_in)

                # else:
                #     rec.sequencee = rec.journal_id.category_code + (3 - len(str(rec.journal_id.sequencee))) * '0' + str(
                #         rec.journal_id.sequencee)
                # rec.category_code = rec.sequence

    @api.model
    def create(self, vals):
        res = super(EditAccountPayment, self).create(vals)
        for rec in res:
            if rec.payment_type == 'inbound':
                rec.journal_id.sequencee_in = rec.journal_id.sequencee_in + 1
            elif rec.payment_type == 'outbound':
                rec.journal_id.sequencee_out = rec.journal_id.sequencee_out + 1
            elif rec.payment_type == 'transfer':
                rec.journal_id.sequencee_out = rec.journal_id.sequencee_out + 1
                rec.destination_journal_id.sequencee_in = rec.destination_journal_id.sequencee_in + 1
        return res








class EditExpenseExpense(models.Model):
    _inherit = 'expense.expense'

    # category_code = fields.Char(string="Code", required=True, default=0)
    sequencee = fields.Char(string="Sequence", readonly=True, default=0, copy=False)

    @api.onchange('journal_id', 'payment_type')
    def sequence_code(self):
        for rec in self:
            if rec.journal_id:
                rec.sequencee = rec.journal_id.category_code + '.OUT/' + (
                        3 - len(str(rec.journal_id.sequencee_out))) * '0' + str(
                    rec.journal_id.sequencee_out)

    @api.model
    def create(self, vals):
        res = super(EditExpenseExpense, self).create(vals)
        for rec in res:
            rec.journal_id.sequencee_out = rec.journal_id.sequencee_out + 1
        return res





class EditReceiveReceive(models.Model):
    _inherit = 'receive.receive'

    # category_code = fields.Char(string="Code", required=True, default=0)
    sequencee = fields.Char(string="Sequence", readonly=True, default=0, copy=False)

    @api.onchange('journal_id', 'payment_type')
    def sequence_code(self):
        for rec in self:
            if rec.journal_id:
                rec.sequencee = rec.journal_id.category_code + '.IN/' + (
                        3 - len(str(rec.journal_id.sequencee_in))) * '0' + str(
                    rec.journal_id.sequencee_in)


    @api.model
    def create(self, vals):
        res = super(EditReceiveReceive, self).create(vals)
        for rec in res:
            rec.journal_id.sequencee_in = rec.journal_id.sequencee_in + 1

        return res


