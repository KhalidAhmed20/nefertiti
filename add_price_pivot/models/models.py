# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    price_unit = fields.Float('Price', readonly=True,store=True)

    def _select(self):
        res = super(AccountInvoiceReport,self)._select()
        select_str = res + """, line.price_unit AS price_unit """
        return select_str

    def _group_by(self):
        return super(AccountInvoiceReport, self)._group_by() + ", line.price_unit"

