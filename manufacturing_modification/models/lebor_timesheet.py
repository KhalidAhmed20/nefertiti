# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class LeborTimeSheet(models.Model):
    _name = 'lebor.timesheet'
    _description = 'Lebor Time Sheet'

    product_id = fields.Many2one(comodel_name="product.product", string="Product", required=False, )
    lot_id = fields.Many2one(comodel_name="stock.production.lot", string="Lot/Serial Number'", required=False, )
    qty_done = fields.Float(string="Produced",  required=False, )
    lebor_timesheet_ids = fields.One2many(comodel_name="lebor.timesheetline", inverse_name="lebor_timesheet_id", string="", required=False, )
    manufactur_id = fields.Many2one(comodel_name="mrp.production", string="", required=False, )


class LeborTimeSheetLine(models.Model):
    _name = 'lebor.timesheetline'
    _description = 'Lebor Time Sheet Line'

    lebor_timesheet_id = fields.Many2one(comodel_name="lebor.timesheet", string="", required=False, )
    employee_id = fields.Many2one('hr.employee', string="Employee Name", required=True, )
    operating_hours = fields.Integer(string="Operating Hours", required=False, default=1)

