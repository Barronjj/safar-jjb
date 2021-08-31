# -*- coding: utf-8 -*-
from odoo import models, fields


class Gabarit_lectra(models.Model):
    _name = 's_gabarit_lectra'
    _description = 'gabarit_lectra'
    _rec_name = 's_name'

    s_name = fields.Char(string="Nom")
    s_commentaire = fields.Text(string='Commentaire')
    s_gabarit = fields.Many2one('product.template', string='Gabarit', ondelete='cascade')
    s_metrage = fields.Float(string='Métrage')
    s_quantite = fields.Integer(string='Quantité')
