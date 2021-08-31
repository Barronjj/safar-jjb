# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Vehicule_generation(models.Model):
    _name = 's_vehicule_generation'
    _description = 'vehicule_generation'
    _rec_name = 's_name'

    s_name = fields.Char(string="Nom")
    s_dt_debut_generation = fields.Date(string='Dt Début génération')
    s_dt_fin_generation = fields.Date(string='Dt Fin Génération')
    s_id_car_generation = fields.Integer(string='id car generation')
    s_marque = fields.Many2one('s_vehicule_marque', string='Marque')
    s_modele = fields.Many2one('s_vehicule_modele', string='Modèle')
