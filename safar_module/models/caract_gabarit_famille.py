# -*- coding: utf-8 -*-
from odoo import models, fields


class Caract_gabarit_famille(models.Model):
    _name = 's_caract_gabarit_famille'
    _description = 'caract_gabarit_famille'
    _rec_name = 's_name'

    s_name = fields.Char(string='Nom')
    s_univers = fields.Many2one('s_vehicule_univers', string="Univers")
