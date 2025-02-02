# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NewModule(models.Model):
    _inherit = 'new_module.new_module'

    name = fields.Char()


