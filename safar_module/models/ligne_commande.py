# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.tools import timedelta


class LigneCommande(models.Model):
    _inherit = 'sale.order.line'

    s_gabarit_1 = fields.Char()
    s_gabarit_2 = fields.Char()
    s_gabarit_3 = fields.Char()
    s_mat_1 = fields.Many2one('product.product', string="Matériau 1")
    s_mat_2 = fields.Many2one('product.product', string="Matériau 2")
    s_mat_3 = fields.Many2one('product.product', string="Matériau 3")
    s_placement_mat_1 = fields.Selection(selection=[('a', 'A'), ('b', 'B'), ('d', 'D')], store="True")
    s_placement_mat_2 = fields.Selection(selection=[('a', 'A'), ('c', 'C'), ('d', 'D'), ('e', 'E')], store="True")
    s_placement_mat_3 = fields.Selection(selection=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E')])
    s_fil_surpiqure = fields.Many2one('product.product')
    s_broderie_nm_fichier = fields.Char()
    # s_ref_client = fields.Char(compute='_compute_ref_client', inverse='_inverse_ref_client',
    #                            store="True", string="Réf. article pour le client")
    s_ref_client = fields.Char(store="True") #compute='_compute_ref_client_order', store="True", string="Réf. article pour le client")
    s_no_ligne_commande = fields.Char(string="Numéro ligne de commande")
    s_configuration = fields.Text()  # Text permet d'avoir un champ plus grand pour du multi-lignes
    # s_description_complete = fields.Text(store="True") #compute='_compute_ref_client_order', store="True")
    s_modele_note = fields.Many2one('s_note_template', store='False')
    s_tx_remise_importateur = fields.Float(string="mt remise pour stat", store='True')
    s_mt_ht_apres_remise_importateur = fields.Monetary(string="mt HT après remise pour stat")
    s_commentaire_production = fields.Text()
    s_abl = fields.Selection(selection=[('oui', 'Oui'), ('non', 'Non')])

    # @api.depends('product_template_id.s_tab_references_client', 'order_partner_id')
    # def _compute_ref_client(self):
    #     for record in self:
    #         ret = record.product_template_id.name
    #         for ref in record.product_template_id.s_tab_references_client:
    #             if ref.s_client == record.order_partner_id:
    #                 ret = ref.s_cd_produit
    #         record.s_ref_client = ret

    # @api.depends('s_configuration')
    # def _compute_description_complete(self):
    #     for record in self:
    #         description = record.name
    #         if record.s_configuration:
    #             description = record.name + '\n' + record.s_configuration
    #
    #         record.s_description_complete = description

    """Colle la config passée en paramètre dans le champ"""
    @api.onchange('s_configuration')
    def coller_config(self):
        if self.s_configuration:
            if self.s_configuration.split('¤')[0] == 's_configuration':
                for line in self.s_configuration.split('£'):
                    field = line.split('¤')[0]
                    value = line.split('¤')[1]
                    if field == "s_mat_1" or field == "s_mat_2" or field == "s_mat_3":
                        mat = self.env['product.product'].search([('default_code', '=', value)], limit=1)
                        if mat:
                            self[field] = mat.id
                        else:
                            mat = self.env['product.product'].search([('name', '=', value)], limit=1)
                            if mat:
                                self[field] = mat.id
                    elif field == "s_fil_surpiqure":
                        mat = self.env['product.product'].search([('default_code', '=', value)], limit=1)
                        if mat:
                            self[field] = mat.id
                        else:
                            mat = self.env['product.product'].search([('name', '=', value)], limit=1)
                            if mat:
                                self[field] = mat.id
                    else:
                        self[field] = value

    @api.onchange('s_mat_1', 's_mat_2', 's_mat_3')
    def compute_placement_mat(self):
        for record in self:
            if record.s_mat_1 and not record.s_mat_2 and not record.s_mat_3:
                record.s_placement_mat_1 = 'b'
                record.s_placement_mat_2 = ''
                record.s_placement_mat_3 = ''
            if record.s_mat_1 and record.s_mat_2 and not record.s_mat_3:
                record.s_placement_mat_1 = 'b'
                record.s_placement_mat_2 = 'c'
                record.s_placement_mat_3 = ''
            if record.s_mat_1 and record.s_mat_2 and record.s_mat_3:
                record.s_placement_mat_1 = 'b'
                record.s_placement_mat_2 = 'd'
                record.s_placement_mat_3 = 'e'

    @api.onchange("s_modele_note")
    def update_note_client(self):
        if self.s_modele_note:
            self.name = self.s_modele_note.s_name

    @api.onchange('product_id')
    def init_dossier_production(self):
        # On regarde dans le product.template
        if self.product_template_id:
            self.s_gabarit_1 = self.product_template_id.s_gabarit_1
            self.s_gabarit_2 = self.product_template_id.s_gabarit_2
            self.s_gabarit_3 = self.product_template_id.s_gabarit_3
            self.s_mat_1 = self.product_template_id.s_mat_1
            self.s_mat_2 = self.product_template_id.s_mat_2
            self.s_mat_3 = self.product_template_id.s_mat_3
            self.s_placement_mat_1 = self.product_template_id.s_placement_mat_1
            self.s_placement_mat_2 = self.product_template_id.s_placement_mat_2
            self.s_placement_mat_3 = self.product_template_id.s_placement_mat_3
            self.s_fil_surpiqure = self.product_template_id.s_fil_surpiqure
            self.s_broderie_nm_fichier = self.product_template_id.s_broderie_nm_fichier
        # puis on regarde dans le product.product
        if self.product_id:
            if self.product_id.s_gabarit_1_pp:
                self.s_gabarit_1 = self.product_id.s_gabarit_1_pp
            if self.product_id.s_gabarit_2_pp:
                self.s_gabarit_2 = self.product_id.s_gabarit_2_pp
            if self.product_id.s_gabarit_3_pp:
                self.s_gabarit_3 = self.product_id.s_gabarit_3_pp
            if self.product_id.s_mat_1_pp:
                self.s_mat_1 = self.product_id.s_mat_1_pp
            if self.product_id.s_mat_2_pp:
                self.s_mat_2 = self.product_id.s_mat_2_pp
            if self.product_id.s_mat_3_pp:
                self.s_mat_3 = self.product_id.s_mat_3_pp
            if self.product_id.s_placement_mat_1_pp:
                self.s_placement_mat_1 = self.product_id.s_placement_mat_1_pp
            if self.product_id.s_placement_mat_2_pp:
                self.s_placement_mat_2 = self.product_id.s_placement_mat_2_pp
            if self.product_id.s_placement_mat_3_pp:
                self.s_placement_mat_3 = self.product_id.s_placement_mat_3_pp
            if self.product_id.s_fil_surpiqure_pp:
                self.s_fil_surpiqure = self.product_id.s_fil_surpiqure_pp
            if self.product_id.s_broderie_nm_fichier_pp:
                self.s_broderie_nm_fichier = self.product_id.s_broderie_nm_fichier_pp

    @api.onchange('product_id', 'product_uom_qty', 'price_unit', 'discount')
    def update_ref_client(self):
        if self.order_id.state == 'done':
            return False
        else:
            cd = self.product_template_id.default_code  # le code par défaut du modèle d'article
            if not cd:
                cd = self.product_id.default_code  # ou le code par défaut de la variante
            lib = self.name  # on reprend le nom par défaut
            tx_remise = 0

            for price in self.order_id.pricelist_id.item_ids.sorted(key=lambda x: x.min_quantity, reverse=True):
                # ajout d'un tri par qté minimum décroissante et on prend la 1ère ligne de prix trouvée dont la qté mini est >= à la qté cdée
                # dans une liste de prix, on a 2 id d'articles, l'un pour le modèle, l'un pour la variante
                # si l'article est une variante, les 2 id sont renseignés
                # si l'article n'a pas de variante, seul l'id du modèle est renseigné
                # donc pour chaque ligne de la liste de prix, on regarde
                # en premier si l'article de la cde correspond à l'id de la variante...
                # on compare les id de variante d'article (product.product) et du modèle d'article (product.template) pour éviter de sélectionner une autre ligne
                if price.product_id and price.product_id == self.product_id and price.product_tmpl_id == self.product_id.product_tmpl_id and self.product_uom_qty >= price.min_quantity:
                    cd = price.s_ref_prdt_client if price.s_ref_prdt_client else cd
                    lib = price.s_lib_prdt_client if price.s_lib_prdt_client else self.product_template_id.name
                    tx_remise = price.s_tx_remise_facturation if price.s_tx_remise_facturation else 0
                    break
                else:
                    # ... et si on a pas trouvé de variante, on regarde l'id du modèle et en même temps que le champ product_id n'est pas renseigné (=pas de variante)
                    if price.product_tmpl_id == self.product_template_id and not price.product_id and self.product_uom_qty >= price.min_quantity:
                        cd = price.s_ref_prdt_client if price.s_ref_prdt_client else cd
                        lib = price.s_lib_prdt_client if price.s_lib_prdt_client else self.product_template_id.name
                        tx_remise = price.s_tx_remise_facturation if price.s_tx_remise_facturation else 0
                        break
            lib2 = lib
            if self.s_configuration:
                lib2 += '\n' + self.s_configuration
            mt_ht_with_discount = (self.price_subtotal * (1 - tx_remise / 100))

            self.s_ref_client = cd
            self.name = lib
            # self.s_description_complete = lib2
            self.s_tx_remise_importateur = tx_remise
            self.s_mt_ht_apres_remise_importateur = mt_ht_with_discount

    # # Permet de modifier s_description_complete pour qu'elle s'ajuste dès qu'on modifie name ou la config
    # @api.onchange("name", "s_configuration")
    # def set_description(self):
    #     if self.name:
    #         if self.s_configuration:
    #             self.s_description_complete = self.name + '\n' + self.s_configuration
    #         else:
    #             self.s_description_complete = self.name  # self.name

    def _inverse_ref_client(self):
        for record in self:
            for ref in record.product_template_id.s_tab_references_client:
                if ref.s_client == record.order_partner_id:
                    ref.s_cd_produit = record.s_ref_client
                else:
                    new_rec = self.env['s_produit_client'].create({
                        's_name': record.s_ref_client,
                        's_article': record.product_template_id.id,
                        's_cd_produit': record.s_ref_client,
                        's_client': record.order_partner_id.id
                    })

    # @api.depends('s_mat_1', 's_mat_2')
    # def _compute_placement_mat(self):
    #     for record in self:
    #         if record.s_mat_1 == record.s_mat_2:
    #             record.s_placement_mat_1 = record.s_placement_mat_2 = 'a'
    #         else:
    #             if record.product_template_id.s_placement_b:
    #                 record.s_placement_mat_1 = 'b'
    #                 record.s_placement_mat_2 = 'c'
    #             else:
    #                 record.s_placement_mat_1 = 'd'
    #                 record.s_placement_mat_2 = 'e'

    # def _prepare_procurement_values(self, group_id=False):
    #     """ Prepare specific key for moves or other components that will be created from a stock rule
    #     comming from a sale order line. This method could be override in order to add other custom key that could
    #     be used in move/po creation."""
    #     values = super(LigneCommande, self)._prepare_procurement_values(group_id)
    #     self.ensure_one()
    #     date_planned = self.order_id.date_order \
    #                    + timedelta(days=self.customer_lead or 0.0) - timedelta(
    #         days=self.order_id.company_id.security_lead)
    #     values.update({
    #         'group_id': group_id,
    #         'sale_line_id': self.id,
    #         'date_planned': date_planned,
    #         'route_ids': self.route_id,
    #         'warehouse_id': self.order_id.warehouse_id or False,
    #         'partner_id': self.order_id.partner_shipping_id.id,
    #         'company_id': self.order_id.company_id,
    #         's_mat_un': self.s_mat_un.id,
    #         's_mat_deux': self.s_mat_deux.id,
    #         's_placement_mat_1': self.s_placement_mat_1,
    #         's_placement_mat_2': self.s_placement_mat_2,
    #     })
    #     for line in self.filtered("order_id.commitment_date"):
    #         date_planned = fields.Datetime.from_string(line.order_id.commitment_date) - timedelta(
    #             days=line.order_id.company_id.security_lead)
    #         values.update({
    #             'date_planned': fields.Datetime.to_string(date_planned),
    #         })
    #     return values

    def _prepare_invoice_line(self):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.
        :param qty: float quantity to invoice
        """
        self.ensure_one()
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'discount': self.discount,
            'price_unit': self.price_unit,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'analytic_account_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)],
            's_init_client': self.order_partner_id.id,
            's_bl_name': self.order_id.name,
        }
        if self.display_type:
            res['account_id'] = False
        return res

    """Ouvre le configurateur SAFAR dans une nouvelle fenetre"""

    def call_safar_config_saleorderline(self):
        url_site = self.env['ir.config_parameter'].get_param('url.configurateur')
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': url_site,
        }


# class StockRule(models.Model):
#     _inherit = 'stock.rule'
#
#     def _get_custom_move_fields(self):
#         record = super(StockRule, self)._get_custom_move_fields()
#         record += ['s_mat_un', 's_mat_deux', 's_placement_mat_1', 's_placement_mat_2']
#         return record
#
#     def _prepare_mo_vals(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values,
#                          bom):
#         date_deadline = fields.Datetime.to_string(self._get_date_planned(product_id, company_id, values))
#         return {
#             'origin': origin,
#             'product_id': product_id.id,
#             'product_qty': product_qty,
#             'product_uom_id': product_uom.id,
#             'location_src_id': self.location_src_id.id or self.picking_type_id.default_location_src_id.id or location_id.id,
#             'location_dest_id': location_id.id,
#             'bom_id': bom.id,
#             'date_deadline': date_deadline,
#             'date_planned_finished': fields.Datetime.from_string(values['date_planned']),
#             'date_planned_start': date_deadline,
#             'procurement_group_id': False,
#             'propagate_cancel': self.propagate_cancel,
#             'propagate_date': self.propagate_date,
#             'propagate_date_minimum_delta': self.propagate_date_minimum_delta,
#             'orderpoint_id': values.get('orderpoint_id', False) and values.get('orderpoint_id').id,
#             'picking_type_id': self.picking_type_id.id or values['warehouse_id'].manu_type_id.id,
#             'company_id': company_id.id,
#             'move_dest_ids': values.get('move_dest_ids') and [(4, x.id) for x in values['move_dest_ids']] or False,
#             'user_id': False,
#             's_mat_un': values.get('s_mat_un'),
#             's_mat_deux': values.get('s_mat_deux'),
#             's_placement_mat_1': values.get('s_placement_mat_1'),
#             's_placement_mat_2': values.get('s_placement_mat_2'),
#         }
