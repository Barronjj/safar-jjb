# -*- coding: utf-8 -*-
from odoo import models, fields


class Univers_gabarit(models.Model):
    _name = 's_univers_gabarit'
    _description = 'univers_gabarit'
    _rec_name = 's_name'

    s_name = fields.Char(string="Nom")
    s_gabarit = fields.Many2one('product.template', string='Gabarit', ondelete='cascade')
    s_univers = fields.Many2one('s_vehicule_univers', string='Univers', ondelete='cascade')
