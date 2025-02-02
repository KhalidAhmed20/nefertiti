# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError



class purchase_order_inh(models.Model):
    _inherit = 'purchase.order'

    type = fields.Char(string="Type", required=False, )
    state = fields.Selection(selection_add=[('shipped', 'Shipped')])

    def get_shipped(self):
        for rec in self:
            if rec.state in ['purchase', 'done']:
                rec.state = 'shipped'


class Newproduct_Module(models.Model):
    _inherit = 'product.category'

    category_code = fields.Char(string="Category Code", required=True, default=0)
    sequence = fields.Integer(string="Sequence", default=1, )


class product_product(models.Model):
    _inherit = 'product.product'

    @api.onchange('categ_id')
    def sequence_code(self):
        for rec in self:
            if rec.categ_id:
                if len(str(rec.categ_id.sequence)) <= 3:
                    rec.default_code = rec.categ_id.category_code + (3 - len(str(rec.categ_id.sequence))) * '0' + str(
                        rec.categ_id.sequence)
                    rec.category_code = rec.default_code
                else:
                    raise UserError(_("The sequence must not exceed three numbers"))

    @api.model
    def create(self, vals):
        res = super(product_product, self).create(vals)
        for rec in res:
            rec.categ_id.sequence = rec.categ_id.sequence + 1

        return res


#
#
class product_template(models.Model):
    _inherit = 'product.template'

    @api.onchange('categ_id')
    def sequence_code(self):
        for rec in self:
            if rec.categ_id:
                if len(str(rec.categ_id.sequence)) <= 3:
                    rec.default_code = rec.categ_id.category_code + (3 - len(str(rec.categ_id.sequence))) * '0' + str(
                        rec.categ_id.sequence)
                    rec.category_code = rec.default_code
                else:
                    raise UserError(_("The sequence must not exceed three numbers"))

    @api.model
    def create(self, vals):
        res = super(product_template, self).create(vals)
        for rec in res:
            rec.categ_id.sequence = rec.categ_id.sequence

        return res
