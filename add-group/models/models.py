# -*- coding: utf-8 -*-

from odoo import models, fields, api


class add_field_hremployee(models.Model):
    _inherit = 'hr.employee'

    employee_code = fields.Char(string="Employee Code", required=False, )
    specialization = fields.Char(string="Specialization", required=False, )
    equipment = fields.Char(string="Equipment No", required=False, )


class add_group_respartner(models.Model):
    _inherit = 'res.partner'

    tags_id = fields.Many2one(comodel_name="res.partner.category", string="Tags", required=False, )


class purchaseorderinh(models.Model):
    _inherit = 'purchase.order'

    tags_id = fields.Many2one(comodel_name="res.partner.category", string="Tags",
                              required=False, related='partner_id.tags_id')


class purchaseorderline(models.Model):
    _inherit = 'purchase.order.line'

    name = fields.Text(string='Description', required=False)

    _sql_constraints = [
        ('accountable_required_fields',
         "CHECK(1=1)",
         "Missing required fields on accountable purchase order line."),
        ('non_accountable_null_fields',
         "CHECK(1=1)",
         "Forbidden values on non-accountable purchase order line"),
    ]


class saleorderinh(models.Model):
    _inherit = 'sale.order'

    tags_id = fields.Many2one(comodel_name="res.partner.category", string="Tags",
                              required=False, related='partner_id.tags_id')
