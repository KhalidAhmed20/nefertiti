# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    active = fields.Boolean(
        default=True, )


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    active = fields.Boolean(
        default=True, )
