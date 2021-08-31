# -*- coding: utf-8 -*-
from odoo import fields, models, api

import logging
_logger = logging.getLogger(__name__)

class MrpWorkcenterProductivity(models.Model):
    _inherit = 'mrp.workcenter.productivity'

    s_operateur = fields.Many2one('hr.employee', string="Opérateur")
    s_qte_realisee = fields.Integer(string='Qté réalisée')
    s_product_id = fields.Many2one(related="production_id.product_id", string="Article", store=True)
    s_categ_id = fields.Many2one(related="production_id.product_id.product_tmpl_id.categ_id", string="Catégorie Article", store=True)
    s_gamme = fields.Many2one(related="production_id.routing_id", string="Gamme", store=True)
    s_of_cd = fields.Char(related="production_id.name", string="OF", store=True)
    s_operation = fields.Char(related="workorder_id.name", string="Opération", store=True)
    s_uo_qte = fields.Float(string="UOxQté")
    s_duration_expected = fields.Float(string="Durée attendue")  # , compute='_compute_duration_expected')
    s_commentaire = fields.Text(string="Commentaire")
    s_cd_binome = fields.Char(string="Cd Binôme")

    @api.model
    def create(self, values):
        record = super(MrpWorkcenterProductivity, self).create(values)

        # on cherche l'OT
        OT = self.env['mrp.workorder'].search([('id', '=', record.workorder_id.id)])
        if OT:
            # on cherche l'Opération pour en récupérer le %UO et la qté
            Ope = self.env['mrp.routing.workcenter'].search([('id', '=', OT.operation_id.id)])
            if Ope:
                # on cherche l'OF pour en récupérer l'unité d'oeuvre
                OF = self.env['mrp.production'].search([('id', '=', OT.production_id.id)])
                if OF:
                    record.s_uo_qte = (record.s_qte_realisee * OF.s_unite_oeuvre * Ope.s_uo_percent / 100)
                    record.s_duration_expected = (record.s_qte_realisee * OF.s_unite_oeuvre * Ope.s_uo_percent / 100) * 100

        # on cherche l'employé pour récupérer son code binôme
        EMP = self.env['hr.employee'].search([('id', '=', record.s_operateur.id)])
        if EMP:
            record.s_cd_binome = EMP.s_cd_binome

        return record

    def write(self, values):
        for suivi in self:
            _logger.info('SUIVI ' + str(suivi.id))
            # on cherche l'OT
            OT = self.env['mrp.workorder'].search([('id', '=', suivi.workorder_id.id)])
            if OT:
                # on cherche l'Opération pour en récupérer le %UO et la qté
                Ope = self.env['mrp.routing.workcenter'].search([('id', '=', OT.operation_id.id)])
                if Ope:
                    # on cherche l'OF pour en récupérer l'unité d'oeuvre
                    OF = self.env['mrp.production'].search([('id', '=', OT.production_id.id)])
                    if OF:
                        if 's_qte_realisee' in values:
                            qty = values.get('s_qte_realisee', 0)
                        else:
                            qty = suivi.s_qte_realisee

                        _logger.info('OF=' + OF.name + '/ OT=' + OT.name + ' / UO=' +
                                     str(OF.s_unite_oeuvre) + ' / %UO=' + str(Ope.s_uo_percent) + ' / Qté=' +
                                     str(qty))

                        values['s_uo_qte'] = (qty * OF.s_unite_oeuvre * Ope.s_uo_percent / 100)
                        values['s_duration_expected'] = (qty * OF.s_unite_oeuvre * Ope.s_uo_percent / 100) * 100

            # on cherche l'employé pour récupérer son code binôme
            EMP = self.env['hr.employee'].search([('id', '=', suivi.s_operateur.id)])
            if EMP:
                values['s_cd_binome'] = EMP.s_cd_binome

            return super(MrpWorkcenterProductivity, suivi).write(values)


