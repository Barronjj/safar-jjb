# -*- coding: utf-8 -*-

# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import tools

from odoo import api, fields, models

class SaleReport(models.Model):
    _inherit = 'sale.report'

    s_report_mt_ht_apres_remise_importateur = fields.Float('Montant HT après remise importateur', readonly=True)
    s_tx_remise_importateur = fields.Float(string="Tx remise importateur pour stat", readonly=True)
    s_ref_client = fields.Char(string="Ref produit client", readonly=True)
    s_no_ligne_commande = fields.Char(string="Numéro ligne de commande", readonly=True)
    s_effective_date = fields.Date(string="Date effective", readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['margin'] = ",sum(l.s_mt_ht_apres_remise_importateur / CASE COALESCE(s.currency_rate, 0) WHEN 0 THEN 1.0 ELSE s.currency_rate END) as s_report_mt_ht_apres_remise_importateur"
        fields['s_tx_remise_importateur'] = ", l.s_tx_remise_importateur"
        fields['s_ref_client'] = ", l.s_ref_client"
        fields['s_no_ligne_commande'] = ", l.s_no_ligne_commande"
        fields['effective_date'] = ", s.effective_date AS s_effective_date"

        groupby=", l.s_tx_remise_importateur, l.s_ref_client, l.s_no_ligne_commande, s.effective_date"

        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)