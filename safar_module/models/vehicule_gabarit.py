# -*- coding: utf-8 -*-
from odoo import models, fields


class Vehicule_gabarit(models.Model):
    _name = 's_vehicule_gabarit'
    _description = 'vehicule_gabarit'
    _rec_name = 's_name'

    s_name = fields.Char(string="Nom")
    s_article_gabarit = fields.Many2one('product.template', string='Article Gabarit', ondelete='cascade')
    s_vehicule = fields.Many2one('s_vehicule', string='Véhicule', ondelete='cascade')
