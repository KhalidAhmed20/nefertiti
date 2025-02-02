# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class Translate_Warehouse(models.Model):
    _inherit = 'stock.warehouse'

    name = fields.Char(required=True, translate=True)


class Translate_location(models.Model):
    _inherit = 'stock.location'

    name = fields.Char(required=True, translate=True)


class Translate_productcategory(models.Model):
    _inherit = 'product.category'

    name = fields.Char('Name', index=True, required=True, translate=True)


class Translate_respartner(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(translate=True)


class Translate_hrdepartment(models.Model):
    _inherit = 'hr.department'

    name = fields.Char(required=True, translate=True)


class Translate_hrjob(models.Model):
    _inherit = 'hr.job'

    name = fields.Char(required=True, translate=True)


class Translate_accountgroup(models.Model):
    _inherit = 'account.group'

    name = fields.Char(required=True, translate=True)

# class Translate_hremployee(models.Model):
#     _inherit = 'hr.employee'
#
#     name = fields.Char(required=True, translate=True)
