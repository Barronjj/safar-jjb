# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Vehicule_serie(models.Model):
    _name = 's_vehicule_serie'
    _description = 'vehicule_serie'
    _rec_name = 's_name'

    s_name = fields.Char(string="Nom")
    s_generation = fields.Many2one('s_vehicule_generation', string='Génération')
    s_id_car_serie = fields.Integer(string='Id car serie')
    s_marque = fields.Many2one('s_vehicule_marque', string='Marque')
    s_modele = fields.Many2one('s_vehicule_modele', string='Modèle')
