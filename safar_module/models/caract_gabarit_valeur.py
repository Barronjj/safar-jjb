# -*- coding: utf-8 -*-
from odoo import models, fields


class Caract_gabarit_valeur(models.Model):
    _name = 's_caract_gabarit_valeur'
    _description = 'caract_gabarit_valeur'
    _rec_name = 's_name'

    s_name = fields.Char(string='Nom')
    s_caracteristique = fields.Many2one('s_caract_gabarit_caracteristique', string='Caractéristique')
    s_famille = fields.Many2one('s_caract_gabarit_famille', string='Famille')
    s_sous_famille = fields.Many2one('s_caract_gabarit_ssfamille', string='Sous-Famille')
    s_univers = fields.Many2one('s_vehicule_univers', string='Univers')
    s_valeur = fields.Char(string='Valeur')
