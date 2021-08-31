# -*- coding: utf-8 -*-
from odoo import fields, models


class Article(models.Model):
    _inherit = 'product.pricelist.item'

    s_ref_prdt_client = fields.Char()
    s_lib_prdt_client = fields.Char()
    s_tx_remise_facturation = fields.Float()
    s_ref_interne_related = fields.Char(related="product_id.default_code", store="False", string="Ref Interne")
