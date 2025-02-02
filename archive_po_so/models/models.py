# -*- coding: utf-8 -*-

from email.policy import default
from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    active = fields.Boolean('active', default=True, groups='base.group_system')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    active = fields.Boolean('active', default=True, groups='base.group_system')


class TransferArchive(models.Model):
    _inherit = 'stock.picking'

    active = fields.Boolean('active', default=True, groups='base.group_system')


class OperationArchive(models.Model):
    _inherit = 'stock.picking.type'

    active = fields.Boolean('active', default=True, groups='base.group_system')


class PaymentArchive(models.Model):
    _inherit = 'account.payment'

    active = fields.Boolean('active', default=True, groups='base.group_system')

