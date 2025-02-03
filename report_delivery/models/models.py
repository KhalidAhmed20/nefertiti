# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    paper_grade = fields.Char(string="Paper Grade", required=False, )
    basic_weight_gms = fields.Char(string="Basic Weight GMS", required=False, )
    roll_width_cm = fields.Char(string="Roll Width CM", required=False, )
    shift = fields.Char(string="Shift", required=False, )
    roll_od_cm = fields.Char(string="Roll O.D (CM)", required=False, )
    core_diameter = fields.Char(string="Core Diameter", required=False, )
    number_of_piles = fields.Char(string="Number Of Piles", required=False, )
    number_of_rolls = fields.Char(string="Number Of Rolls", required=False, )
    color = fields.Char(string="Color", required=False, )
    no_of_joints = fields.Char(string="No Of Joints", required=False, )
    weight_kg = fields.Char(string="Weight Kg", required=False, )
    code_number = fields.Char(string="Code Number", required=False, )
    production_date = fields.Date(string="Production Date", required=False, )

    # def barcode_data(self):
    #     data = ''
    #     for rec in self:
    #         data += 'Name %s ' % rec.company_id.name or rec.company_id.partner_id.name
    #         data += '\n'
    #         data += 'VAT No.  %s ' % rec.company_id.partner_id.vat
    #         data += '\n'
    #         data += 'Amount Tax %s ' % rec.currency_id.symbol
    #         data += '\n'
    #         data += 'Total %s' % rec.currency_id.symbol
    #         data += '\n'
    #         data += 'Date  %s' % str(rec.production_date)
    #     return data
