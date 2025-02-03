import datetime

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta



class MaintenanceRequestInherit(models.Model):
    _inherit = "maintenance.request"

    maintenance_equipment_ids = fields.One2many('maintenance.equipment.lines', 'maintenance_request_id',
                                                string="المعدات المرتبطة")

    name = fields.Char(string='Title', required=True,
                       readonly=True, default=lambda self: _('New'))

    duration = fields.Float(string="Duration Time (Hours)", compute='_compute_duration_time',store=True)
    request_date = fields.Datetime(string="Request Date")
    close_date = fields.Datetime(string="Close Date")
    code = fields.Char(string="كود")
    machine_number = fields.Char(string="رقم الماكينة")
    unit_of_measure = fields.Char(string="وحدة القياس")
    product = fields.Float()
    quantity = fields.Float()
    stock_picking_id = fields.Many2one('stock.picking')
    is_repaired = fields.Boolean(string="Is Repaired", default=True)
    is_create = fields.Boolean(default=False)
    in_progres = fields.Boolean(default=False)

    def create_request(self):
        trans = self.env['stock.picking']
        doc = {
            'location_id': 24,
            'location_dest_id': 110,
            'picking_type_id': 82,
            'maintenance_request_id': self.id
        }
        s = trans.create(doc)
        self.stock_picking_id = s
        for line in self.maintenance_equipment_ids:
            s.write({'move_ids_without_package': [(0, 0,
                                                   {
                                                       'product_id': line.product_id.id,
                                                       'product_uom_qty': line.quantity_replaced,
                                                       'name': line.product_id.name,
                                                       'product_uom': line.product_id.uom_id.id,
                                                       'location_id': 24,
                                                       'location_dest_id': 18,
                                                   })],
                     'move_lines': [(0, 0, {
                         'product_id': line.product_id.id,
                         'product_uom_qty': line.quantity_replaced,
                         'name': line.product_id.name,
                         'product_uom': line.product_id.uom_id.id,
                         'location_id': 24,
                         'location_dest_id': 18,
                     })]
                     })
        s.action_assign()
        self.request_date = fields.Datetime.now()
        self.in_progres = True
        self.is_create = True

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'maintenance.request') or _('New')
        res = super(MaintenanceRequestInherit, self).create(vals)
        return res

    @api.depends('request_date', 'close_date')
    def _compute_duration_time(self):
        for record in self:
            if record.request_date and record.close_date:
                duration =  record.close_date - record.request_date
                record.duration = duration.total_seconds() / 3600
            else:
                record.duration_time = 0

    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        if self.equipment_id:
            self.maintenance_equipment_ids = [(5, 0, 0)]
            self.code = self.equipment_id.code
            self.machine_number = self.equipment_id.machine_number
            for equipment in self.equipment_id.maintenance_equipment_ids:
                self.maintenance_equipment_ids = [(0, 0, {
                    'product_id': equipment.product_id.id,
                    'product_qty': equipment.product_qty,
                    'quantity_replaced': equipment.quantity_replaced,
                    'product_location': equipment.product_location,
                    'unit_of_measure': equipment.unit_of_measure,
                    'reserved': equipment.reserved,
                    'maintenance_request_id': self.id,
                    'stock_from_domain': equipment.stock_from_domain.ids
                })]
            for rec in self.maintenance_equipment_ids:
                domain = []
                if rec.product_id.qty_available > 0:
                    for loc in rec.product_id.stock_quant_ids:
                        domain.append(loc.location_id.id)
                    dd = [('id', 'in', domain)]
                    rec.stock_from_domain = domain
                else:
                    rec.stock_from_domain = None

    def repaired(self):
        if self.stock_picking_id.state != 'done':
            raise ValidationError("The equipment repair cannot be performed until the stock move is in Done state.")
        for line in self.maintenance_equipment_ids:
            vals = ({
                'name':self.name,
                'equipment_sequence':self.equipment_id.name,
                'product_id': line.product_id.id,
                'product_qty': line.product_qty,
                'quantity_replaced': line.quantity_replaced,
                'unit_of_measure': line.unit_of_measure,
                'reserved': line.reserved,
                'stock_from': 24,
                'stock_to': 18,
                'maintenance_request_id': self.id,
            })
            record = self.env['maintenance.equipment.line'].create(vals).sudo()

        if self.stage_id.id != 2:
            raise ValidationError("The repair cannot be performed until the order status is 'In Progress'.")
        self.is_repaired = False
        self.stage_id = 3
        self.close_date = fields.Datetime.now()


    def in_progress(self):
        if self.stock_picking_id.state != 'done':
            raise ValidationError("The equipment repair cannot be performed until the stock move is in Done state.")
        self.stage_id = 2
        self.in_progres = False
        self.request_date = fields.Datetime.now()

class picking(models.Model):
    _inherit = 'stock.picking'

    maintenance_request_id = fields.Many2one('maintenance.request')

    def button_validate(self):
        res = super(picking, self).button_validate()
        if self.maintenance_request_id:
            self.maintenance_request_id.is_repaired = True
            self.is_repaired = False
        return res


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    maintenance_equipment_ids = fields.One2many('maintenance.equipment.lines', 'maintenance_equipment_id',
                                                create=False, string="خطوط المعدات")

    code = fields.Char(string="كود")
    machine_number = fields.Char(string="رقم الماكينة")
    unit_of_measure = fields.Char(string="وحدة القياس")
    quantity = fields.Float(string="الكمية")
    product_id = fields.Many2one('product.product', string="المنتج")


class MaintenanceEquipmentLines(models.Model):
    _name = "maintenance.equipment.lines"

    maintenance_request_id = fields.Many2one("maintenance.request", string="طلب الصيانة")
    stock_from = fields.Many2one('stock.location', string="من")
    stock_to = fields.Many2one('stock.location', string="الى")
    maintenance_equipment_id = fields.Many2one('maintenance.equipment')
    product_id = fields.Many2one('product.product', string="المنتج")
    product_qty = fields.Float(string="الكمية")
    stock_from_domain = fields.Many2many('stock.location')
    cost = fields.Float(string="التكلفة")
    unit_of_measure = fields.Char()
    quantity_replaced = fields.Float(string="الكمية المستبدلة")
    product_location = fields.Many2one('stock.location', related='product_id.property_stock_production',
                                       string="المخزن")
    reserved = fields.Float(string="المستهلك")
    cost = fields.Float(compute="_compute_cost", string="التكلفة")
    coast = fields.Float(compute="_compute_coast", string="التكلفة المستبدلة")

    def _compute_cost(self):
        for rec in self:
            rec.cost = rec.product_qty * rec.product_id.standard_price

    def _compute_coast(self):
        for rec in self:
            rec.coast = rec.quantity_replaced * rec.product_id.standard_price

    @api.onchange('product_id')
    def ppp(self):
        if self.product_id.uom_id.name:
            self.unit_of_measure = self.product_id.uom_id.name
        if self.product_id.standard_price:
            self.cost = self.product_id.standard_price
        for rec in self:
            domain = []
            if rec.product_id.qty_available > 0:
                for loc in rec.product_id.stock_quant_ids:
                    domain.append(loc.location_id.id)
                dd = [('id', 'in', domain)]
                rec.stock_from_domain = domain

            else:
                rec.stock_from_domain = None


class MaintenanceEquipmentLine(models.Model):
    _name = "maintenance.equipment.line"

    @api.onchange('product_id')
    def domain_default(self):
        for rec in self:
            domain = []
            if rec.product_id.qty_available > 0:
                for loc in rec.product_id.stock_quant_ids:
                    domain.append(loc.location_id.id)
                dd = [('id', 'in', domain)]
                rec.stock_from_domain = domain

            else:
                rec.stock_from_domain = None

    name = fields.Char(readonly=True, string="Sequence")
    equipment_sequence = fields.Char(readonly=True, string="Equipment")
    product_id = fields.Many2one('product.product', string="المنتج")
    product_qty = fields.Float(string="الكمية")
    quantity_replaced = fields.Float(string="الكمية المستبدلة")
    product_location = fields.Many2one('stock.location', related='product_id.property_stock_production',
                                       string="المخزن")
    unit_of_measure = fields.Char()
    reserved = fields.Float(string="المستهلك")
    maintenance_equipment_id = fields.Many2one("maintenance.equipment", string="المعدات")
    maintenance_request_id = fields.Many2one("maintenance.request", string="طلب الصيانة")
    stock_from_domain = fields.Many2many('stock.location')
    stock_from = fields.Many2one('stock.location', string="من")
    stock_to = fields.Many2one('stock.location', string="الى")
    cost = fields.Float(compute="_compute_cost", string="التكلفة")
    coast = fields.Float(compute="_compute_coast", string="التكلفة المستبدلة")

    def _compute_cost(self):
        for rec in self:
            rec.cost = rec.product_qty * rec.product_id.standard_price

    def _compute_coast(self):
        for rec in self:
            rec.coast = rec.quantity_replaced * rec.product_id.standard_price
