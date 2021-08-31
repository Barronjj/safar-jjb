# -*- coding: utf-8 -*-
from odoo import models, fields


class Produit_client(models.Model):
    _name = 's_produit_client'
    _description = 'produit_client'
    _rec_name = 's_name'

    s_name = fields.Char(string="Libellé de l’article pour le client")
    s_article = fields.Many2one('product.template', string='Article', ondelete='cascade')
    s_cd_produit = fields.Char(string='Réf. article pour le client')
    s_client = fields.Many2one('res.partner', string='Client', ondelete='cascade')
