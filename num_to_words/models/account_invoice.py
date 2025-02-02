# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from num2words import num2words



class AccountInvoice(models.Model):
    _inherit = "account.move"

    text_amount = fields.Char(string="Montant en lettre", required=False, compute="amount_to_words", )






    @api.depends('amount_total')
    def amount_to_words(self):
        for rec in self:
            if rec.company_id.text_amount_language_currency:
                rec.text_amount= rec._l10n_pe_edi_amount_to_text()
            else:
                rec.text_amount=rec.text_amount


    @api.model
    def _l10n_pe_edi_amount_to_text(self):
        """Transform a float amount to text words on peruvian format: AMOUNT IN TEXT 11/100
        :returns: Amount transformed to words peruvian format for invoices
        :rtype: str
        """
        self.ensure_one()
        amount_i, amount_d = divmod(self.amount_total, 1)
        a = self.company_id.text_amount_language_currency
        words = num2words(amount_i, lang = a)
        if a == "ar":
            words= words.replace('،', ' و')
        elif a == "en":
            words = words.replace(',', ' and')
        result = words + ' ' + self.currency_id.currency_unit_label
        return result




    # @api.depends('order_line.price_total')
    # def _amount_all(self):
    #     """
    #     Compute the total amounts of the SO.
    #     """
    #     for order in self:
    #         amount_untaxed = amount_tax = 0.0
    #         for line in order.order_line:
    #             amount_untaxed += line.price_subtotal
    #             amount_tax += line.price_tax
    #         order.update({
    #             'amount_untaxed': amount_untaxed,
    #             'amount_tax': amount_tax,
    #             'amount_total': amount_untaxed + amount_tax,
    #         })
    # res.update({'resend_invitation': True})
