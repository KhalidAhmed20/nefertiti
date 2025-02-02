# -*- coding: utf-8 -*-

from odoo import models, fields


class OrdersLineCustomize(models.Model):
    _inherit = 'sale.order.line'

    product_size = fields.Many2one('sale.product_size', string="Size", required=1)
    product_gram = fields.Many2one('sale.product_gram', string="Gram", required=1)
    product_layers = fields.Many2one('sale.product_layers', string="Layers", required=1)
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', required=1)

    def _prepare_invoice_line(self, **optional_values):
        invoice_line = super(OrdersLineCustomize, self)._prepare_invoice_line(**optional_values)
        invoice_line['analytic_account_id'] = self.analytic_account_id.id
        return invoice_line


class SaleReport(models.Model):
    _inherit = 'sale.report'

    product_size = fields.Many2one('sale.product_size', string="Size")
    product_gram = fields.Many2one('sale.product_gram', string="Gram")
    product_layers = fields.Many2one('sale.product_layers', string="Layers")

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
            min(l.id) as id,
            l.product_id as product_id,
            t.uom_id as product_uom,
            sum(l.product_uom_qty / u.factor * u2.factor) as product_uom_qty,
            sum(l.qty_delivered / u.factor * u2.factor) as qty_delivered,
            sum(l.qty_invoiced / u.factor * u2.factor) as qty_invoiced,
            sum(l.qty_to_invoice / u.factor * u2.factor) as qty_to_invoice,
            sum(l.price_total / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as price_total,
            sum(l.price_subtotal / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as price_subtotal,
            sum(l.untaxed_amount_to_invoice / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as untaxed_amount_to_invoice,
            sum(l.untaxed_amount_invoiced / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as untaxed_amount_invoiced,
            count(*) as nbr,
            s.name as name,
            s.date_order as date,
            s.state as state,
            s.partner_id as partner_id,
            s.user_id as user_id,
            s.company_id as company_id,
            s.campaign_id as campaign_id,
            s.medium_id as medium_id,
            s.source_id as source_id,
            extract(epoch from avg(date_trunc('day',s.date_order)-date_trunc('day',s.create_date)))/(24*60*60)::decimal(16,2) as delay,
            t.categ_id as categ_id,
            s.pricelist_id as pricelist_id,
            s.analytic_account_id as analytic_account_id,
            s.team_id as team_id,
            p.product_tmpl_id,
            partner.country_id as country_id,
            partner.industry_id as industry_id,
            partner.commercial_partner_id as commercial_partner_id,
            sum(p.weight * l.product_uom_qty / u.factor * u2.factor) as weight,
            sum(p.volume * l.product_uom_qty / u.factor * u2.factor) as volume,
            l.discount as discount,
            sum((l.price_unit * l.product_uom_qty * l.discount / 100.0 / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END)) as discount_amount,
            s.id as order_id,
            l.product_size,
            l.product_gram,
            l.product_layers
        """

        for field in fields.values():
            select_ += field

        from_ = """
                sale_order_line l
                      join sale_order s on (l.order_id=s.id)
                      join res_partner partner on s.partner_id = partner.id
                        left join product_product p on (l.product_id=p.id)
                            left join product_template t on (p.product_tmpl_id=t.id)
                    left join uom_uom u on (u.id=l.product_uom)
                    left join uom_uom u2 on (u2.id=t.uom_id)
                    left join product_pricelist pp on (s.pricelist_id = pp.id)
                %s
        """ % from_clause

        groupby_ = """
            l.product_id,
            l.order_id,
            t.uom_id,
            t.categ_id,
            s.name,
            s.date_order,
            s.partner_id,
            s.user_id,
            s.state,
            s.company_id,
            s.campaign_id,
            s.medium_id,
            s.source_id,
            s.pricelist_id,
            s.analytic_account_id,
            s.team_id,
            p.product_tmpl_id,
            partner.country_id,
            partner.industry_id,
            partner.commercial_partner_id,
            l.discount,
            s.id %s,
            l.product_size,
            l.product_gram,
            l.product_layers
        """ % (groupby)
        return '%s (SELECT %s FROM %s WHERE l.product_id IS NOT NULL GROUP BY %s)' % (with_, select_, from_, groupby_)

    # def _select_additional_fields(self):
    #     res = super()._select_additional_fields()
    #     res['product_size'] = "l.product_size"
    #     # res['product_gram'] = "l.product_gram"
    #     # res['product_layers'] = "l.product_layers"
    #     return res
    #
    # def _group_by_sale(self):
    #     res = super()._group_by_sale()
    #     res += """,
    #         l.product_size"""
    #     return res


class SaleProductSize(models.Model):
    _name = 'sale.product_size'

    name = fields.Char(string="Name", required=1)


class SaleProductGram(models.Model):
    _name = 'sale.product_gram'

    name = fields.Char(string="Name", required=1)


class SaleProductLayers(models.Model):
    _name = 'sale.product_layers'

    name = fields.Char(string="Name", required=1)
