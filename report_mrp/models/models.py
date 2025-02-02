# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ReportMrp(models.Model):
    _name = 'report.mrp'
    _description = 'Report Mrp'

    name = fields.Char()
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
    mrp_production_id = fields.Many2one(comodel_name="mrp.production", string="", required=False, )
    lot_id = fields.Many2one('stock.production.lot', 'Lot/Serial Number', required=False, )


class MrpProductionInherit(models.Model):
    _inherit = 'mrp.production'

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
    mrp_production_ids = fields.One2many(comodel_name="report.mrp", inverse_name="mrp_production_id", string="",
                                         required=False, )
    lot_id = fields.Many2one('stock.production.lot', 'Lot/Serial Number', required=False,compute='get_l_lot_id' )


    @api.depends('finished_move_line_ids')
    def get_l_lot_id(self):
        self.lot_id=False
        for rec in self:
            for line in rec.finished_move_line_ids:
                if line.lot_id:
                    rec.lot_id=line.lot_id.id
                else:
                    rec.lot_id =rec.lot_id


    def get_line_report_delivery(self):
        return {
            'name': _('Report Delivery'),
            'view_mode': 'tree',
            'res_model': 'report.mrp',
            'type': 'ir.actions.act_window',
            'domain': [('id', '=', self.mrp_production_ids.ids)],
        }



class mrp_product_produce(models.TransientModel):
    _inherit = 'mrp.product.produce.line'

    @api.onchange('product_id')
    def get_default_lot_x(self):
        for rec in self:
            if rec.product_id:
                rec.lot_id=self.env['stock.production.lot'].search([('product_id', '=', self.product_id.id)], limit=1)




class mrp_product_produce(models.TransientModel):
    _inherit = 'mrp.product.produce'

    def do_produce(self):
        self.get_weight_kg()
        return super(mrp_product_produce, self).do_produce()

    def continue_production(self):
        self.get_weight_kg()
        return super(mrp_product_produce, self).continue_production()

    def get_weight_kg(self):
        for rec in self:
            rec.production_id.weight_kg = rec.qty_producing
            rec.production_id.mrp_production_ids = [(0, 0, {
                "paper_grade": rec.production_id.paper_grade,
                "basic_weight_gms": rec.production_id.basic_weight_gms,
                "roll_width_cm": rec.production_id.roll_width_cm,
                "shift": rec.production_id.shift,
                "roll_od_cm": rec.production_id.roll_od_cm,
                "core_diameter": rec.production_id.core_diameter,
                "number_of_piles": rec.production_id.number_of_piles,
                "number_of_rolls": rec.production_id.number_of_rolls,
                "color": rec.production_id.color,
                "no_of_joints": rec.production_id.no_of_joints,
                "weight_kg": rec.production_id.weight_kg,
                "code_number": rec.production_id.code_number,
                "production_date": rec.production_id.production_date,
            })]
