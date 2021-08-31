# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    def annuler_ligne_bl_reservee_par_planificateur(self):
        # pour chaque ligne de l'onglet opérations détaillées du BL
        # concernant un article stocké (#)
        # ayant une qté réservée <> 0
        # et une qté faite = 0
        list_line = self.env['stock.move.line'].search(['&', '&', '&',
                                                        ('product_id.product_tmpl_id.name', 'like', '%#%'),
                                                        ('product_uom_qty', '!=', 0),
                                                        ('qty_done', '=', 0),
                                                        ('write_uid', '=', 1)])

        for line in list_line:
        # on cherche la ligne correspondante dans l'onglet opérations
            move = self.env['stock.move'].search([('id', '=', line.move_id.id)])
            if move:
                # on retire de la qté réservée de l'opération, la qté réservée de l'opération détaillée
                move.reserved_availability = move.reserved_availability - line.product_uom_qty
                # on repasse le statut de Assigned à Confirmed
                move.state = 'confirmed'
                # on supprime la ligne de l'opération détaillée
                line.unlink()