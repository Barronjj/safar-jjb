# -*- coding: utf-8 -*-
from odoo import fields, models, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sh_mrp_ids = fields.Many2many(
        comodel_name='mrp.production',
        string="Ordre de fabrication",
        compute='_compute_mrp_orders'
    )

    @api.model
    def create(self, values):
        record = super(StockPicking, self).create(values)

        # on ajoute par défaut le transporteur GLS au BL
        company = self.env['res.company'].search([('id', '=', record.company_id.id)])
        if company:
            if company.s_methode_expe_par_defaut:
                record.carrier_id = company.s_methode_expe_par_defaut.id

        return record

    def _compute_mrp_orders(self):
        if self:
            for rec in self:
                mrp_orders = self.env['mrp.production'].sudo().search([
                    ('origin', '=', rec.origin)
                ])
                if mrp_orders:
                    rec.sh_mrp_ids = [(6, 0, mrp_orders.ids)]
                else:
                    rec.sh_mrp_ids = False
