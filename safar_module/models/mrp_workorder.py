# -*- coding: utf-8 -*-
from odoo import fields, models  # , api

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    s_categ_id = fields.Many2one(related="production_id.product_id.product_tmpl_id.categ_id", string="Catégorie Article", store=True)
    s_uo_qte = fields.Float(string="UOxQté")

    # le write est appelé lorsqu'on clique sur le bouton plan de l'OF
    def write(self, values):
        # on cherche l'Opération pour en récupérer le %UO et la qté
        Ope = self.env['mrp.routing.workcenter'].search([('id', '=', self.operation_id.id)])
        if Ope:
            # on cherche l'OF pour en récupérer l'unité d'oeuvre
            OF = self.env['mrp.production'].search([('id', '=', self.production_id.id)])
            if OF:
                if 'qty_production' in values:
                    qty = values.get('qty_production', 0)
                else:
                    qty = self.qty_production

                values['s_uo_qte'] = (qty * OF.s_unite_oeuvre * Ope.s_uo_percent / 100)
                values['duration_expected'] = (qty * OF.s_unite_oeuvre * Ope.s_uo_percent / 100) * 100

        return super(MrpWorkorder, self).write(values)

    # @api.model
    # def create(self, values):
    #     record = super(MrpWorkorder, self).create(values)
    #
    #     # on cherche l'Opération pour en récupérer le %UO et la qté
    #     Ope = self.env['mrp.routing.workcenter'].search([('id', '=', record.operation_id.id)])
    #     if Ope:
    #         # on cherche l'OF pour en récupérer l'unité d'oeuvre
    #         OF = self.env['mrp.production'].search([('id', '=', record.production_id.id)])
    #         if OF:
    #             record.s_uo_qte = (record.qty_production * OF.s_unite_oeuvre * Ope.s_uo_percent / 100)
    #             record.duration_expected = (record.qty_production * OF.s_unite_oeuvre * Ope.s_uo_percent / 100) * 100
    #     return record