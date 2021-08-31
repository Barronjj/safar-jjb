# -*- coding: utf-8 -*-
from odoo import models, fields


class Caract_gabarit_ssfamille(models.Model):
    _name = 's_caract_gabarit_ssfamille'
    _description = 'caract_gabarit_ssfamille'
    _rec_name = 's_name'

    s_name = fields.Char(string='Nom')
    s_famille = fields.Many2one('s_caract_gabarit_famille', string="Famille")
    s_univers = fields.Many2one('s_vehicule_univers', string="Univers")
