# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MrpWorkcenterLine(models.Model):
    _name = 'mrp.workcenter.line'
    _description = 'Mrp Work center Line'

    employee_id = fields.Many2one('hr.employee', string="Employee Name", required=True, )
    operating_hours = fields.Integer(string="Operating Oours", required=False, default=1)
    hourly_cost = fields.Float(string="Hourly Cost", required=False, )
    total_cost = fields.Float(string="Total Cost", required=False, )
    mrp_workcenter_id = fields.Many2one(comodel_name="mrp.workcenter", string="", required=False, readonly=True)
    bom_id = fields.Many2one(comodel_name="mrp.workcenter", string="", required=False, readonly=True)
    production_id = fields.Many2one(comodel_name="mrp.production", string="", required=False, readonly=True)

    @api.onchange('operating_hours', 'employee_id')
    def get_total_cost(self):
        employee_salary = self.env['hr.contract'].sudo().search([('employee_id', '=', self.employee_id.id)])
        salary = employee_salary.wage
        for rec in self:
            rec.hourly_cost = salary / 26 / 7
            rec.total_cost = rec.operating_hours * rec.hourly_cost


class MrpWorkcenterInherit(models.Model):
    _inherit = 'mrp.workcenter'

    mrp_workcenter_ids = fields.One2many(comodel_name="mrp.workcenter.line", inverse_name="mrp_workcenter_id",
                                         string="", required=False, )
    coast_per_hour = fields.Float(string="Cost Per Hour", required=False, )

    @api.onchange('mrp_workcenter_ids', 'coast_per_hour')
    def get_total_coast(self):
        for rec in self:
            rec.costs_hour = 0
            for line in rec.mrp_workcenter_ids:
                rec.costs_hour += line.total_cost
            rec.costs_hour += rec.coast_per_hour


class MrpBomLine(models.Model):
    _name = 'mrp.bom.lin'
    _description = 'New Description'

    product_tmpl_id = fields.Many2one('mrp.workcenter', string="Machine Name", required=True, )
    operating_hours = fields.Integer(string="Operating Oours", required=False, default=1)
    machine_cost = fields.Float(string="Machine Cost", required=False, )
    total_cost = fields.Float(string="Total Cost", required=False, )
    mrp_bom_id = fields.Many2one(comodel_name="mrp.bom", string="", required=False, readonly=True)
    mrp_productions_id = fields.Many2one(comodel_name="mrp.production", string="", required=False, readonly=True)

    @api.onchange('operating_hours', 'product_tmpl_id', 'machine_cost')
    def get_total_cost_machine(self):
        for rec in self:
            rec.total_cost = rec.operating_hours * rec.machine_cost


class MrpBomInherit(models.Model):
    _inherit = 'mrp.bom'

    mrp_bom_ids = fields.One2many(comodel_name="mrp.bom.lin", inverse_name="mrp_bom_id", string="", required=False, )
    mrp_boms_ids = fields.One2many(comodel_name="mrp.workcenter.line", inverse_name="bom_id", string="",
                                   required=False, readonly=True,store=True)

    @api.onchange('mrp_bom_ids')
    def get_labore_machin(self):
        for rec in self:
            for line in rec.mrp_bom_ids:
                rec.mrp_boms_ids = line.product_tmpl_id.mrp_workcenter_ids.ids


class MrpBomLines(models.Model):
    _name = 'mrp.bom.lines'
    _description = 'New Description'

    product_tmpl_id = fields.Many2one('mrp.workcenter', string="Machine Name", required=True, )
    employee_id = fields.Many2one('hr.employee', string="Employee Name", required=True, )
    operating_hours = fields.Integer(string="Operating Oours", required=False, default=1)
    hourly_cost = fields.Float(string="Hourly Cost", required=False, )
    total_cost = fields.Float(string="Total Cost", required=False, )
    mrp_boms_id = fields.Many2one(comodel_name="mrp.bom", string="", required=False, readonly=True)
    mrp_production_id = fields.Many2one(comodel_name="mrp.production", string="", required=False, readonly=True)

    @api.onchange('operating_hours', 'employee_id')
    def get_total_cost(self):
        employee_salary = self.env['hr.contract'].sudo().search([('employee_id', '=', self.employee_id.id)])
        salary = employee_salary.wage
        for rec in self:
            rec.hourly_cost = salary / 26 / 7
            rec.total_cost = rec.operating_hours * rec.hourly_cost


class MrpProductionInherit(models.Model):
    _inherit = 'mrp.production'

    mrp_production_ids = fields.One2many(comodel_name="mrp.workcenter.line", inverse_name="production_id",
                                         string="",
                                         required=False, readonly=False)
    mrp_productions_ids = fields.One2many(comodel_name="mrp.bom.lin", inverse_name="mrp_productions_id", string="",
                                          required=False, )

#
#
    @api.onchange('mrp_productions_ids')
    def get_labore_machin_production(self):
        for rec in self:
            for line in rec.mrp_productions_ids:
                rec.mrp_production_ids = line.product_tmpl_id.mrp_workcenter_ids.ids
#
#
#
    @api.constrains('bom_id')
    def get_lebors_machine(self):
        for rec in self:
            if rec.bom_id:
                for line in rec.bom_id.mrp_boms_ids:
                    line.production_id=rec.id
                rec.mrp_productions_ids =[(6,0,rec.bom_id.mrp_bom_ids.ids)]
#
#
#
    def get_finished_product(self):
        return {
            'name': _('Finished Product'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('manufactur_id', 'in', [a.id for a in self])],
            'res_model': 'lebor.timesheet',
        }




class partialproductionqt(models.TransientModel):
    _inherit = 'partial.production.qty'



    def do_partial_produce(self):
        res=super(partialproductionqt, self).do_partial_produce()
        for rec in self:
            mirna=self.env['lebor.timesheet'].sudo().create({
        'product_id': rec.product_id.id,
        'lot_id': rec.finished_lot_id.id,
        'qty_done': rec.partial_qty,
        'manufactur_id': rec.production_id.id,
    })
        return res
