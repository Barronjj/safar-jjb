# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    def get_products_refclient(self, products, quantities, partners, date=False, uom_id=False):
        """ For a given pricelist, return ref client for products
        Returns: dict{product_id: product price}, in the given pricelist """
        self.ensure_one()
        return {
            product_id: res_tuple[0]
            for product_id, res_tuple in self._compute_price_rule(
                list(zip(products, quantities, partners)),
                date=date,
                uom_id=uom_id
            ).items()
        }