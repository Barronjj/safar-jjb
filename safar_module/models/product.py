# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # s_ref_prdt_client_ctx = fields.Char(string='Ref Client', compute='_compute_product_ref_clt') #, inverse='_set_product_ref_clt')
    s_ligne_1_label_pp = fields.Char()
    s_gabarit_1_pp = fields.Char()
    s_gabarit_2_pp = fields.Char()
    s_gabarit_3_pp = fields.Char()
    s_mat_1_pp = fields.Many2one('product.product')
    s_mat_2_pp = fields.Many2one('product.product')
    s_mat_3_pp = fields.Many2one('product.product')
    s_placement_mat_1_pp = fields.Selection(selection=[('a', 'A'), ('b', 'B'), ('d', 'D')], store="True")
    s_placement_mat_2_pp = fields.Selection(selection=[('a', 'A'), ('c', 'C'), ('e', 'E')], store="True")
    s_placement_mat_3_pp = fields.Selection(selection=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E')])
    s_fil_surpiqure_pp = fields.Many2one('product.product')
    s_broderie_nm_fichier_pp = fields.Char()
    s_abl_pp = fields.Selection(selection=[('oui', 'Oui'), ('non', 'Non')])

    # @api.depends_context('pricelist', 'partner', 'quantity', 'uom', 'date', 'no_variant_attributes_price_extra')
    # def _compute_product_ref_clt(self):
    #     prices = {}
    #     pricelist_id_or_name = self._context.get('pricelist')
    #     if pricelist_id_or_name:
    #         pricelist = None
    #         partner = self.env.context.get('partner', False)
    #         quantity = self.env.context.get('quantity', 1.0)
    #
    #         # Support context pricelists specified as list, display_name or ID for compatibility
    #         if isinstance(pricelist_id_or_name, list):
    #             pricelist_id_or_name = pricelist_id_or_name[0]
    #         if isinstance(pricelist_id_or_name, str):
    #             pricelist_name_search = self.env['product.pricelist'].name_search(pricelist_id_or_name, operator='=', limit=1)
    #             if pricelist_name_search:
    #                 pricelist = self.env['product.pricelist'].browse([pricelist_name_search[0][0]])
    #         elif isinstance(pricelist_id_or_name, int):
    #             pricelist = self.env['product.pricelist'].browse(pricelist_id_or_name)
    #
    #         if pricelist:
    #             quantities = [quantity] * len(self)
    #             partners = [partner] * len(self)
    #             # prices = pricelist.s_ref_prdt_client
    #             refs = pricelist.get_products_refclient(self, quantities, partners)
    #
    #     for product in self:
    #         product.s_ref_prdt_client_ctx = prices.get(product.id, 0.0)

    # def _set_product_price(self):
    #     for product in self:
    #         if self._context.get('uom'):
    #             value = self.env['uom.uom'].browse(self._context['uom'])._compute_price(product.price, product.uom_id)
    #         else:
    #             value = product.price
    #         value -= product.price_extra
    #         product.write({'list_price': value})