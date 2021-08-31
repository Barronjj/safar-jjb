# -*- coding: utf-8 -*-
from odoo import fields, models, api
from datetime import datetime

class Article(models.Model):
    _inherit = 'product.template'

    s_accompagnement = fields.Boolean()
    s_ajouter_mousse = fields.Boolean()
    s_colisage = fields.Integer()
    s_configuration_a_la_cde = fields.Selection(selection=[('complete', 'Complète'), ('limitee', 'Limitée')])
    s_dispo_configurateur = fields.Boolean()
    s_dispo_simulateur = fields.Boolean()
    s_gabarit_materiau = fields.Selection(selection=[('gab', 'Gabarit'), ('mat', 'Matériau'), ('fil', 'Fil'), ('aut', 'Autre')])
    s_type_matiere = fields.Selection(selection=[('tis', 'Tissu'), ('sim', 'Simili'), ('alc', 'Alcane'), ('aut', 'Autre')])
    s_etiquette_airbag_ct = fields.Boolean()
    s_etiquette_consigne = fields.Boolean()
    s_hauteur_cm = fields.Integer()
    s_laize_cm = fields.Integer()
    s_largeur_cm = fields.Integer()
    s_longueur_cm = fields.Integer()
    s_partie_centrale = fields.Boolean()
    s_poids = fields.Float()
    s_tab_caract_gabarit_val = fields.Many2many('s_caract_gabarit_valeur')
    s_tab_ref_lectra = fields.One2many('s_gabarit_lectra', 's_gabarit')
    s_tab_references_client = fields.One2many('s_produit_client', 's_article')
    s_univers_autorises = fields.One2many('s_univers_gabarit', 's_gabarit')
    s_article_marche = fields.Many2one('s_article_marche')
    s_vehicules = fields.One2many('s_vehicule_gabarit', 's_article_gabarit', string="Véhicules")
    s_unite_oeuvre = fields.Float()
    s_modele_associe = fields.Many2many('s_article_modele_associe')
    s_nomenclature_douaniere = fields.Char()
    s_gabarit_1 = fields.Char()
    s_gabarit_2 = fields.Char()
    s_gabarit_3 = fields.Char()
    s_mat_1 = fields.Many2one('product.product', string="Matériau 1")
    s_mat_2 = fields.Many2one('product.product', string="Matériau 2")
    s_mat_3 = fields.Many2one('product.product', string="Matériau 3")
    s_placement_mat_1 = fields.Selection(selection=[('a', 'A'), ('b', 'B'), ('d', 'D')], store="True")
    s_placement_mat_2 = fields.Selection(selection=[('a', 'A'), ('c', 'C'), ('e', 'E')], store="True")
    s_placement_mat_3 = fields.Selection(selection=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E')])
    s_fil_surpiqure = fields.Many2one('product.product')
    s_broderie_nm_fichier = fields.Char()
    s_ligne_1_label = fields.Char()
    s_laize_utile = fields.Integer()
    s_laize_utile_bis = fields.Integer()
    s_abl = fields.Selection(selection=[('oui', 'Oui'), ('non', 'Non')])
    s_categorie_pdr = fields.Many2one('s_article_categorie_pdr')
    s_cd_delai_fabrication = fields.Many2one('s_delai_fabrication')
    s_nom_simulateur = fields.Char(string="Nom d'affichage")

    def write(self, values):
        if 's_unite_oeuvre' in values:
            list_of = self.env['mrp.production'].search([('product_id.product_tmpl_id', '=', self.id)])
            for of in list_of:
                of_vals = []
                of_vals = {
                    's_unite_oeuvre': values.get('s_unite_oeuvre', 0),
                    's_uo_qte': values.get('s_unite_oeuvre', 0) * of.product_qty,
                }

                if of_vals:
                    of.write(of_vals)

        return super(Article, self).write(values)

    @api.onchange('s_cd_delai_fabrication')
    def onchange_cd_delai_fabrication(self):
        if self.s_cd_delai_fabrication.s_duree_jr:
            self.sale_delay = self.s_cd_delai_fabrication.s_duree_jr