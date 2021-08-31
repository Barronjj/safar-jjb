# -*- coding: utf-8 -*-
from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # product_id = fields.Many2one(inverse='find_dossier_prod_article')
    s_of_gesprod = fields.Char(string="OF Gesprod")
    s_tab_placement = fields.One2many('s_placement_of', 's_of_id', 'Placements')
    s_commentaire_of = fields.Text(string="Commentaire OF")
    s_gabarit_1 = fields.Char(string="Gabarit 1")
    s_gabarit_2 = fields.Char(string="Gabarit 2")
    s_gabarit_3 = fields.Char(string="Gabarit 3")
    s_mat_1 = fields.Many2one('product.product', string="Matériau 1")
    s_mat_2 = fields.Many2one('product.product', string="Matériau 2")
    s_mat_3 = fields.Many2one('product.product', string="Matériau 3")
    s_fil_surpiqure = fields.Many2one('product.product', string="Fil surpiqûre")
    s_broderie_nm_fichier = fields.Char(string="Broderie")
    s_id_cde = fields.Many2one('sale.order', string="Cde Id")
    s_id_ligne_cde = fields.Many2one('sale.order.line', string="Cde Ligne Id")
    s_ligne_1_label = fields.Char(string="Etiquette Ligne 1")
    s_mat_type_1 = fields.Char(string="Matériau 1 Type")
    s_mat_type_2 = fields.Char(string="Matériau 2 Type")
    s_config = fields.Boolean(string="Présence Configuration")
    s_unite_oeuvre = fields.Float(string="Unité d\'oeuvre")
    s_uo_qte = fields.Float(string="UOxQté")
    s_abl = fields.Selection(selection=[('oui', 'Oui'), ('non', 'Non')], string="Présence ABL")
    s_of_prepare = fields.Boolean(string="Préparé")
    s_categ_id = fields.Many2one(related="product_id.product_tmpl_id.categ_id", string="Catégorie Article", store=True)

    """CODE récupéré depuis application achetée sur le store 'Sale order quick MRP information'"""

    def action_view_order(self):
        return {
            'name': 'Manufacturing Orders',
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.production',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current'
        }

    """Fin du code acheté"""

    def button_etiq_sato(self):
        return self.env.ref('safar_module.action_report_label_sato').report_action(self)

    def button_etiq_datamax(self):
        return self.env.ref('safar_module.action_report_label_datamax').report_action(self)

    @api.model
    def create(self, values):
        record = super(MrpProduction, self).create(values)
        # le principe, on crée une ligne de placement par matière
        # pour chaque ligne de cde (normalement une seule), on recherche le quadruplet: id article + gabarit + matiere + qte
        # si on le trouve, on récupère la ligne entière
        # si on ne trouve pas, on ajoute manuellement la ligne de matière en concaténant les gabarits
        if record.move_dest_ids:
            for move in record.move_dest_ids:
                if move.sale_line_id:
                    # on mémorise l'id de la cde et de la ligne pour pouvoir récupérer des infos pour les étiquettes
                    if not record.s_id_cde:
                        record.s_id_cde = move.sale_line_id.order_id
                    if not record.s_id_ligne_cde:
                        record.s_id_ligne_cde = move.sale_line_id.id

                    # on forme le gabarit ou la suite de gabarit pour la recherche des placements
                    gab = ""
                    if move.sale_line_id.s_gabarit_1:
                        gab = move.sale_line_id.s_gabarit_1
                        record.s_gabarit_1 = move.sale_line_id.s_gabarit_1
                    if move.sale_line_id.s_gabarit_2:
                        gab = gab + ' + ' + move.sale_line_id.s_gabarit_2
                        record.s_gabarit_2 = move.sale_line_id.s_gabarit_2
                    if move.sale_line_id.s_gabarit_3:
                        gab = gab + ' + ' + move.sale_line_id.s_gabarit_3
                        record.s_gabarit_3 = move.sale_line_id.s_gabarit_3

                    gamme_name = ""
                    if record.routing_id:
                        gamme_name = record.routing_id.name.upper()

                    if 'COVER' in gamme_name:
                        # on est sur un cover donc on récupère tous les placements du dernier OF concernant le même article
                        last_of = self.env['mrp.production'].search(
                            [('product_id', '=', move.sale_line_id.product_id.id), ('id', '!=', record.id)],
                            order="id desc", limit=1)
                        if last_of:
                            list_placement = self.env['s_placement_of'].search([('s_of_id', '=', last_of.id)])
                            # on copie chaque placement du dernier OF
                            for placement in list_placement:
                                placement_vals = []
                                placement_vals = {
                                    's_of_id': record.id,
                                    's_gabarit': placement.s_gabarit,
                                    'display_name': placement.s_gabarit,
                                    's_matiere': placement.s_matiere.id,
                                    's_type': placement.s_type,
                                    's_qte': move.sale_line_id.product_uom_qty,
                                    's_laize': placement.s_laize,
                                    's_lettre': placement.s_lettre,
                                    's_metrage': placement.s_metrage,
                                    's_nb_epaisseur': move.sale_line_id.product_uom_qty,
                                    's_nom_placement': placement.s_nom_placement,
                                }
                                if placement_vals:
                                    self.env['s_placement_of'].create(placement_vals)
                    else:
                        # on est sur autre chose qu'un cover, donc on travaille ligne de placement par ligne de placement
                        # creer une ligne par Gabarit + MATERIAU + lettre + qte
                        # rechercher sur Gabarit + LAIZE + lettre + qte
                        # on parcoure les 3 matières possibles
                        for y in range(1, 4):
                            field_mat = "s_mat_" + str(y)
                            field_placement = "s_placement_mat_" + str(y)
                            if move.sale_line_id[field_mat]:
                                # on cherche dans l'apprentissage
                                old_placement = self.env['s_placement_of'].search(['&', '&', '&',
                                                                                   ('s_gabarit', '=', gab),
                                                                                   ('s_laize', '=',
                                                                                    move.sale_line_id[
                                                                                        field_mat].s_laize_utile),
                                                                                   ('s_lettre', '=',
                                                                                    move.sale_line_id[field_placement]),
                                                                                   ('s_qte', '=',
                                                                                    move.sale_line_id.product_uom_qty)],
                                                                                  order='id desc', limit=1)

                                if not old_placement:
                                    # on cherche une 2ème fois avec la laize utile bis (zoho 327)
                                    old_placement = self.env['s_placement_of'].search(['&', '&', '&',
                                                                                       ('s_gabarit', '=', gab),
                                                                                       ('s_laize', '=',
                                                                                        move.sale_line_id[
                                                                                            field_mat].s_laize_utile_bis),
                                                                                       ('s_lettre', '=',
                                                                                        move.sale_line_id[
                                                                                            field_placement]),
                                                                                       ('s_qte', '=',
                                                                                        move.sale_line_id.product_uom_qty)],
                                                                                      order='id desc', limit=1)

                                placement_vals = []
                                if old_placement:
                                    placement_vals = {
                                        's_of_id': record.id,
                                        's_gabarit': old_placement.s_gabarit,
                                        'display_name': old_placement.s_gabarit,
                                        's_matiere': move.sale_line_id[field_mat].id,
                                        's_type': old_placement.s_type,
                                        's_qte': old_placement.s_qte,
                                        's_laize': old_placement.s_laize,
                                        's_lettre': old_placement.s_lettre,
                                        's_metrage': old_placement.s_metrage,
                                        's_nb_epaisseur': old_placement.s_nb_epaisseur,
                                        's_nom_placement': old_placement.s_nom_placement,
                                    }
                                else:
                                    placement_vals = {
                                        's_of_id': record.id,
                                        's_gabarit': gab,
                                        'display_name': gab,
                                        's_matiere': move.sale_line_id[field_mat].id,
                                        's_laize': move.sale_line_id[field_mat].s_laize_utile,
                                        's_qte': move.sale_line_id.product_uom_qty,
                                        's_lettre': move.sale_line_id[field_placement],
                                    }

                                if placement_vals:
                                    self.env['s_placement_of'].create(placement_vals)

                    # suite de l'onglet dossier production
                    if move.sale_line_id.s_mat_1:
                        record['s_mat_1'] = move.sale_line_id.s_mat_1
                        record['s_mat_type_1'] = move.sale_line_id.s_mat_1.categ_id.name
                    if move.sale_line_id.s_mat_2:
                        record['s_mat_2'] = move.sale_line_id.s_mat_2
                        record['s_mat_type_2'] = move.sale_line_id.s_mat_2.categ_id.name
                    if move.sale_line_id.s_mat_3:
                        record['s_mat_3'] = move.sale_line_id.s_mat_3
                    if move.sale_line_id.s_fil_surpiqure:
                        record['s_fil_surpiqure'] = move.sale_line_id.s_fil_surpiqure
                    if move.sale_line_id.s_broderie_nm_fichier:
                        record['s_broderie_nm_fichier'] = move.sale_line_id.s_broderie_nm_fichier

                    # info pour les étiquettes
                    if move.sale_line_id.s_configuration:
                        record.s_ligne_1_label = move.sale_line_id.s_configuration.split('\n')[0]
                        record.s_config = True
                    else:
                        if move.sale_line_id.product_id.s_ligne_1_label_pp:
                            record.s_ligne_1_label = move.sale_line_id.product_id.s_ligne_1_label_pp
                        else:
                            if move.sale_line_id.product_id.s_ligne_1_label:
                                record.s_ligne_1_label = move.sale_line_id.product_id.s_ligne_1_label
                            else:
                                record.s_ligne_1_label = move.sale_line_id.product_id.name
                        record.s_config = False

                    # on mémorise le commentaire de production de l'article dans le commentaire de l'OF
                    if move.sale_line_id.s_commentaire_production:
                        record.s_commentaire_of = move.sale_line_id.s_commentaire_production

                    # on mémorise l'unité d'oeuvre de l'article
                    if record.product_id.product_tmpl_id.s_unite_oeuvre:
                        record.s_unite_oeuvre = record.product_id.product_tmpl_id.s_unite_oeuvre
                        record.s_uo_qte = record.product_id.product_tmpl_id.s_unite_oeuvre * record.product_qty

                    # on mémorise la présence d'un ABL de l'article
                    if record.product_id.product_tmpl_id.s_abl:
                        record.s_abl = record.product_id.product_tmpl_id.s_abl
        else:
            # Si pas de ligne de cde, cela signifie que c'est un OF manuel (ou réappro)
            # pour chaque champ, on regarde d'abord s'il y a une valeur au niveau product.product
            # sinon dans le niveau product.template
            if record.product_id.s_gabarit_1_pp:
                record["s_gabarit_1"] = record.product_id.s_gabarit_1_pp
            else:
                if record.product_id.s_gabarit_1:
                    record["s_gabarit_1"] = record.product_id.s_gabarit_1
                else:
                    record["s_gabarit_1"] = ""
            if record.product_id.s_gabarit_2_pp:
                record["s_gabarit_2"] = record.product_id.s_gabarit_2_pp
            else:
                if record.product_id.s_gabarit_2:
                    record["s_gabarit_2"] = record.product_id.s_gabarit_2
                else:
                    record["s_gabarit_2"] = ""
            if record.product_id.s_gabarit_3_pp:
                record["s_gabarit_3"] = record.product_id.s_gabarit_3_pp
            else:
                if record.product_id.s_gabarit_3:
                    record["s_gabarit_3"] = record.product_id.s_gabarit_3
                else:
                    record["s_gabarit_3"] = ""
            if record.product_id.s_mat_1_pp:
                record['s_mat_1'] = record.product_id.s_mat_1_pp
                record['s_mat_type_1'] = record.product_id.s_mat_1_pp.categ_id.name
            else:
                if record.product_id.s_mat_1:
                    record['s_mat_1'] = record.product_id.s_mat_1
                    record['s_mat_type_1'] = record.product_id.s_mat_1.categ_id.name
                else:
                    record['s_mat_1'] = False
                    record['s_mat_type_1'] = ""
            if record.product_id.s_mat_2_pp:
                record['s_mat_2'] = record.product_id.s_mat_2_pp
                record['s_mat_type_2'] = record.product_id.s_mat_2_pp.categ_id.name
            else:
                if record.product_id.s_mat_2:
                    record['s_mat_2'] = record.product_id.s_mat_2
                    record['s_mat_type_2'] = record.product_id.s_mat_2.categ_id.name
                else:
                    record['s_mat_2'] = False
                    record['s_mat_type_2'] = ""
            if record.product_id.s_mat_3_pp:
                record['s_mat_3'] = record.product_id.s_mat_3_pp
            else:
                if record.product_id.s_mat_3:
                    record['s_mat_3'] = record.product_id.s_mat_3
                else:
                    record['s_mat_3'] = False
            if record.product_id.s_fil_surpiqure_pp:
                record['s_fil_surpiqure'] = record.product_id.s_fil_surpiqure_pp
            else:
                if record.product_id.s_fil_surpiqure:
                    record['s_fil_surpiqure'] = record.product_id.s_fil_surpiqure
                else:
                    record['s_fil_surpiqure'] = False
            if record.product_id.s_broderie_nm_fichier_pp:
                record['s_broderie_nm_fichier'] = record.product_id.s_broderie_nm_fichier_pp
            else:
                if record.product_id.s_broderie_nm_fichier:
                    record['s_broderie_nm_fichier'] = record.product_id.s_broderie_nm_fichier
                else:
                    record['s_broderie_nm_fichier'] = ""
            # info pour les étiquettes
            if record.product_id.s_ligne_1_label_pp:
                record.s_ligne_1_label = record.product_id.s_ligne_1_label_pp
            else:
                if record.product_id.s_ligne_1_label:
                    record.s_ligne_1_label = record.product_id.s_ligne_1_label
                else:
                    record.s_ligne_1_label = record.product_id.name
            # on mémorise l'unité d'oeuvre de l'article
            if record.product_id.product_tmpl_id.s_unite_oeuvre:
                record.s_unite_oeuvre = record.product_id.product_tmpl_id.s_unite_oeuvre
                record.s_uo_qte = record.product_id.product_tmpl_id.s_unite_oeuvre * record.product_qty

            # on mémorise la présence d'un ABL de l'article
            if record.product_id.s_abl_pp:
                record.s_abl = record.product_id.s_abl_pp
            else:
                if record.product_id.s_abl:
                    record.s_abl = record.product_id.s_abl

                    # on forme le gabarit ou la suite de gabarit pour la recherche des placements
            gab = ""
            if record.s_gabarit_1:
                gab = record.s_gabarit_1
            if record.s_gabarit_2:
                gab = gab + ' + ' + record.s_gabarit_2
            if record.s_gabarit_3:
                gab = gab + ' + ' + record.s_gabarit_3

            qty = 1
            if record.product_qty > 0:
                qty = record.product_qty

            # on supprime les placements existants car dès la sélection du produit, les placements sont créés
            # donc si on change de produit, il faut supprimer les premiers
            record.s_tab_placement = [(5, 0, 0)]

            gamme_name = ""
            nomenclature = record.env['mrp.bom'].search(
                [('product_tmpl_id', '=', record.product_id.product_tmpl_id.id)],
                order="id desc", limit=1)
            if nomenclature:
                if nomenclature.routing_id:
                    gamme_name = nomenclature.routing_id.name.upper()

            if 'COVER' in gamme_name:
                # on est sur un cover donc on récupère tous les placements du dernier OF concernant le même article
                last_of = self.env['mrp.production'].search(
                    [('product_id', '=', record.product_id.id), ('id', '!=', record.id)], order="id desc", limit=1)
                if last_of:
                    list_placement = self.env['s_placement_of'].search([('s_of_id', '=', last_of.id)])
                    for placement in list_placement:
                        placement_vals = []
                        placement_vals = {
                            's_of_id': record.id,
                            's_gabarit': placement.s_gabarit,
                            'display_name': placement.s_gabarit,
                            's_matiere': placement.s_matiere.id,
                            's_type': placement.s_type,
                            's_qte': qty,
                            's_laize': placement.s_laize,
                            's_lettre': placement.s_lettre,
                            's_metrage': placement.s_metrage,
                            's_nb_epaisseur': qty,
                            's_nom_placement': placement.s_nom_placement,
                        }

                        if placement_vals:
                            self.env['s_placement_of'].create(placement_vals)
            else:
                # on est sur autre chose qu'un cover, donc on travaille ligne de placement par ligne de placement
                # creer une ligne par Gabarit + MATERIAU + lettre + qte
                # rechercher sur Gabarit + LAIZE + lettre + qte
                # on parcoure les 3 matériaux possibles
                for y in range(1, 4):
                    field_mat = "s_mat_" + str(y)
                    field_placement = "s_placement_mat_" + str(y)

                    if record[field_mat].id:
                        # on cherche dans l'apprentissage
                        old_placement = self.env['s_placement_of'].search(['&', '&', '&',
                                                                           ('s_gabarit', '=', gab),
                                                                           ('s_laize', '=',
                                                                            record.product_id[field_mat].s_laize_utile),
                                                                           ('s_lettre', '=',
                                                                            record.product_id[field_placement]),
                                                                           ('s_qte', '=', qty)],
                                                                          order='id desc', limit=1)

                        if not old_placement:
                            # on cherche une 2ème fois avec la laize utile bis (zoho 327)
                            old_placement = self.env['s_placement_of'].search(['&', '&', '&',
                                                                               ('s_gabarit', '=', gab),
                                                                               ('s_laize', '=',
                                                                                record.product_id[
                                                                                    field_mat].s_laize_utile_bis),
                                                                               ('s_lettre', '=',
                                                                                record.product_id[field_placement]),
                                                                               ('s_qte', '=', qty)],
                                                                              order='id desc', limit=1)

                        # on ajoute le placement
                        placement_vals = []
                        if old_placement:
                            placement_vals = {
                                's_of_id': record.id,
                                's_gabarit': old_placement.s_gabarit,
                                'display_name': old_placement.s_gabarit,
                                's_matiere': record[field_mat].id,
                                's_type': old_placement.s_type,
                                's_qte': old_placement.s_qte,
                                's_laize': old_placement.s_laize,
                                's_lettre': old_placement.s_lettre,
                                's_metrage': old_placement.s_metrage,
                                's_nb_epaisseur': old_placement.s_nb_epaisseur,
                                's_nom_placement': old_placement.s_nom_placement,
                            }
                        else:
                            placement_vals = {
                                's_of_id': record.id,
                                's_gabarit': gab,
                                'display_name': gab,
                                's_matiere': record[field_mat].id,
                                's_laize': record[field_mat].s_laize_utile,
                                's_qte': qty,
                                's_lettre': record.product_id[field_placement],
                            }

                        if placement_vals:
                            record.env['s_placement_of'].create(placement_vals)

        return record


    # En cas de changement de la qté de l'OF, on la reporte dans les lignes de placement et on relance la recherche de l'apprentissage
    @api.onchange('product_qty')
    def update_qty_placement(self):
        # on mémorise l'unité d'oeuvre de l'article
        if self.product_id.product_tmpl_id.s_unite_oeuvre:
            self.s_uo_qte = self.product_id.product_tmpl_id.s_unite_oeuvre * self.product_qty

        for placement in self.s_tab_placement:
            placement.s_qte = self.product_qty
            old_placement = self.env['s_placement_of'].search(['&', '&',
                                                               '&', ('s_of_id.product_id', '=', self.product_id.id),
                                                               ('s_gabarit', '=', placement.s_gabarit),
                                                               ('s_matiere', '=', placement.s_matiere.id),
                                                               ('s_qte', '=', placement.s_qte)],
                                                              order='id desc', limit=1)

            placement_vals = []
            if old_placement:
                placement_vals = {
                    's_type': old_placement.s_type,
                    's_laize': old_placement.s_laize,
                    's_lettre': old_placement.s_lettre,
                    's_metrage': old_placement.s_metrage,
                    's_nb_epaisseur': old_placement.s_nb_epaisseur,
                    's_nom_placement': old_placement.s_nom_placement,
                }
            else:
                placement_vals = {
                    's_type': "",
                    's_metrage': "",
                    's_nb_epaisseur': "",
                    's_nom_placement': "",
                }

            if placement_vals:
                placement.write(placement_vals)

    @api.onchange('s_mat_1')
    def find_type_mat1(self):
        if self.s_mat_1:
            self.s_mat_type_1 = self.s_mat_1.categ_id.name

    @api.onchange('s_mat_2')
    def find_type_mat2(self):
        if self.s_mat_2:
            self.s_mat_type_2 = self.s_mat_2.categ_id.name

    # def _get_moves_raw_values(self):
    #     moves = []
    #     for production in self:
    #         factor = production.product_uom_id._compute_quantity(production.product_qty,
    #                                                              production.bom_id.product_uom_id) / production.bom_id.product_qty
    #         boms, lines = production.bom_id.explode(production.product_id, factor,
    #                                                 picking_type=production.bom_id.picking_type_id)
    #         if self.s_mat_1.name:
    #             for bom_line, line_data in lines:
    #                 if bom_line.child_bom_id and bom_line.child_bom_id.type == 'phantom' or \
    #                         bom_line.product_id.type not in ['product', 'consu']:
    #                     continue
    #                 if str(self.s_placement_mat_1).capitalize() + str(self.s_mat_1.s_laize_cm) == str(bom_line.product_id.name):
    #                     moves.append(production._get_move_raw_values_custom(bom_line, line_data, self.s_mat_1))
    #                 if str(self.s_placement_mat_2).capitalize() + str(self.s_mat_2.s_laize_cm) == str(bom_line.product_id.name):
    #                     moves.append(production._get_move_raw_values_custom(bom_line, line_data, self.s_mat_2))
    #         else:
    #             for bom_line, line_data in lines:
    #                 if bom_line.child_bom_id and bom_line.child_bom_id.type == 'phantom' or \
    #                         bom_line.product_id.type not in ['product', 'consu']:
    #                     continue
    #                 moves.append(production._get_move_raw_values(bom_line, line_data))
    #     return moves

    def _get_move_raw_values_custom(self, bom_line, line_data, materiau):
        quantity = line_data['qty']
        # alt_op needed for the case when you explode phantom bom and all the lines will be consumed in the operation given by the parent bom line
        alt_op = line_data['parent_line'] and line_data['parent_line'].operation_id.id or False
        source_location = self.location_src_id
        data = {
            'sequence': bom_line.sequence,
            'name': self.name,
            'reference': self.name,
            'date': self.date_planned_start,
            'date_expected': self.date_planned_start,
            'bom_line_id': bom_line.id,
            'picking_type_id': self.picking_type_id.id,
            'product_id': materiau.id,
            'product_uom_qty': quantity,
            'product_uom': materiau.uom_id.id,
            'location_id': source_location.id,
            'location_dest_id': self.product_id.with_context(
                force_company=self.company_id.id).property_stock_production.id,
            'raw_material_production_id': self.id,
            'company_id': self.company_id.id,
            'operation_id': bom_line.operation_id.id or alt_op,
            'price_unit': bom_line.product_id.standard_price,
            'procure_method': 'make_to_stock',
            'origin': self.name,
            'state': 'draft',
            'warehouse_id': source_location.get_warehouse().id,
            'group_id': self.procurement_group_id.id,
            'propagate_cancel': self.propagate_cancel,
        }
        return data

    # -------- BASCULE ---------
    # Fonction utilisée uniquement pour la bascule et appelée manuellement par CRON inactif
    # pour tout OF dont le s_of_gesprod est renseigné et contient %Non commencé%
    # si pas de gabarit1 dans OF:
    # - si Gabarit1 renseigné dans le dossier de production de la fiche de l'article associé :
    #  - renseigner tout le dossier de prod de l'OF avec celui de la fiche article (Gabarit 1, 2, 3, matériaux, ...)
    # - sinon, si Gabarit 1 renseigné dans la ligne de commande :
    #  - prendre le dossier de production dans la ligne d'article associée
    def bascule_report_dossier_prod(self):
        list_of = self.env['mrp.production'].search([('s_of_gesprod', 'like', '%Non commencé%')])
        for record in list_of:
            if not record.s_gabarit_1:
                if record.product_id.product_tmpl_id.s_gabarit_1:
                    record.s_ligne_1_label = record.product_id.product_tmpl_id.s_ligne_1_label
                    record.s_gabarit_1 = record.product_id.product_tmpl_id.s_gabarit_1
                    record.s_gabarit_2 = record.product_id.product_tmpl_id.s_gabarit_2
                    record.s_gabarit_3 = record.product_id.product_tmpl_id.s_gabarit_3
                    record.s_mat_1 = record.product_id.product_tmpl_id.s_mat_1
                    record.s_mat_2 = record.product_id.product_tmpl_id.s_mat_2
                    record.s_mat_3 = record.product_id.product_tmpl_id.s_mat_3
                    record.s_placement_mat_1 = record.product_id.product_tmpl_id.s_placement_mat_1
                    record.s_placement_mat_2 = record.product_id.product_tmpl_id.s_placement_mat_2
                    record.s_placement_mat_3 = record.product_id.product_tmpl_id.s_placement_mat_3
                    record.s_fil_surpiqure = record.product_id.product_tmpl_id.s_fil_surpiqure
                    record.s_broderie_nm_fichier = record.product_id.product_tmpl_id.s_broderie_nm_fichier
                    record.s_abl = record.product_id.product_tmpl_id.s_abl
                else:
                    if record.move_dest_ids:
                        for move in record.move_dest_ids:
                            if move.sale_line_id:
                                # on mémorise l'id de la cde et de la ligne pour pouvoir récupérer des infos pour les étiquettes
                                if not record.s_id_cde:
                                    record.s_id_cde = move.sale_line_id.order_id
                                if not record.s_id_ligne_cde:
                                    record.s_id_ligne_cde = move.sale_line_id.id

                                # on forme le gabarit ou la suite de gabarit pour la recherche des placements
                                gab = ""
                                if move.sale_line_id.s_gabarit_1:
                                    gab = move.sale_line_id.s_gabarit_1
                                    record.s_gabarit_1 = move.sale_line_id.s_gabarit_1
                                if move.sale_line_id.s_gabarit_2:
                                    gab = gab + ' + ' + move.sale_line_id.s_gabarit_2
                                    record.s_gabarit_2 = move.sale_line_id.s_gabarit_2
                                if move.sale_line_id.s_gabarit_3:
                                    gab = gab + ' + ' + move.sale_line_id.s_gabarit_3
                                    record.s_gabarit_3 = move.sale_line_id.s_gabarit_3

                                # creer une ligne par Gabarit + MATERIAU + lettre + qte
                                # rechercher sur Gabarit + LAIZE + lettre + qte
                                # on parcoure les 3 matières possibles
                                if not record.s_tab_placement:  # uniquement si aucun placement n'existe
                                    for y in range(1, 4):
                                        field_mat = "s_mat_" + str(y)
                                        field_placement = "s_placement_mat_" + str(y)

                                        if move.sale_line_id[field_mat]:
                                            # on cherche dans l'apprentissage
                                            old_placement = self.env['s_placement_of'].search(['&', '&', '&',
                                                                                               ('s_gabarit', '=', gab),
                                                                                               ('s_laize', '=',
                                                                                                move.sale_line_id[
                                                                                                    field_mat].s_laize_utile),
                                                                                               ('s_lettre', '=',
                                                                                                move.sale_line_id[
                                                                                                    field_placement]),
                                                                                               ('s_qte', '=',
                                                                                                move.sale_line_id.product_uom_qty)],
                                                                                              order='id desc', limit=1)

                                            placement_vals = []
                                            if old_placement:
                                                placement_vals = {
                                                    's_of_id': record.id,
                                                    's_gabarit': old_placement.s_gabarit,
                                                    'display_name': old_placement.s_gabarit,
                                                    's_matiere': move.sale_line_id[field_mat].id,
                                                    's_type': old_placement.s_type,
                                                    's_qte': old_placement.s_qte,
                                                    's_laize': old_placement.s_laize,
                                                    's_lettre': old_placement.s_lettre,
                                                    's_metrage': old_placement.s_metrage,
                                                    's_nb_epaisseur': old_placement.s_nb_epaisseur,
                                                    's_nom_placement': old_placement.s_nom_placement,
                                                }
                                            else:
                                                placement_vals = {
                                                    's_of_id': record.id,
                                                    's_gabarit': gab,
                                                    'display_name': gab,
                                                    's_matiere': move.sale_line_id[field_mat].id,
                                                    's_laize': move.sale_line_id[field_mat].s_laize_utile,
                                                    's_qte': move.sale_line_id.product_uom_qty,
                                                    's_lettre': move.sale_line_id[field_placement],
                                                }

                                            if placement_vals:
                                                self.env['s_placement_of'].create(placement_vals)

                                # suite de l'onglet dossier production
                                if move.sale_line_id.s_mat_1:
                                    record['s_mat_1'] = move.sale_line_id.s_mat_1
                                    record['s_mat_type_1'] = move.sale_line_id.s_mat_1.categ_id.name
                                if move.sale_line_id.s_mat_2:
                                    record['s_mat_2'] = move.sale_line_id.s_mat_2
                                    record['s_mat_type_2'] = move.sale_line_id.s_mat_2.categ_id.name
                                if move.sale_line_id.s_mat_3:
                                    record['s_mat_3'] = move.sale_line_id.s_mat_3
                                if move.sale_line_id.s_fil_surpiqure:
                                    record['s_fil_surpiqure'] = move.sale_line_id.s_fil_surpiqure
                                if move.sale_line_id.s_broderie_nm_fichier:
                                    record['s_broderie_nm_fichier'] = move.sale_line_id.s_broderie_nm_fichier

                                # info pour les étiquettes
                                if move.sale_line_id.s_configuration:
                                    record.s_ligne_1_label = move.sale_line_id.s_configuration.split('\n')[0]
                                    record.s_config = True
                                else:
                                    if move.sale_line_id.product_id.s_ligne_1_label:
                                        record.s_ligne_1_label = move.sale_line_id.product_id.s_ligne_1_label
                                    else:
                                        record.s_ligne_1_label = move.sale_line_id.product_id.name
                                    record.s_config = False

                                # on mémorise le commentaire de production de l'article dans le commentaire de l'OF
                                if move.sale_line_id.s_commentaire_production:
                                    record.s_commentaire_of = move.sale_line_id.s_commentaire_production

                                # on mémorise l'unité d'oeuvre de l'article
                                if record.product_id.product_tmpl_id.s_unite_oeuvre:
                                    record.s_unite_oeuvre = record.product_id.product_tmpl_id.s_unite_oeuvre
                                    record.s_uo_qte = record.product_id.product_tmpl_id.s_unite_oeuvre * record.product_qty

                                # on mémorise la présence d'un ABL de l'article
                                if record.product_id.product_tmpl_id.s_abl:
                                    record.s_abl = record.product_id.product_tmpl_id.s_abl