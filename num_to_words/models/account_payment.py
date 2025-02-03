# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from num2words import num2words


class AccountPaymentInherit(models.Model):
    _inherit = "account.payment"

    text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words_payment", )

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
