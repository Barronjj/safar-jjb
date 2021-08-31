# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Vehicule_finition(models.Model):
    _name = 's_vehicule_finition'
    _description = 'vehicule_finition'
    _rec_name = 's_name'

    s_name = fields.Char(string="Nom")
    s_annee = fields.Integer(string='Année')
    s_generation = fields.Many2one('s_vehicule_generation', string='Génération')
    s_id_car_equipement = fields.Integer(string='id car equipement')
    s_marque = fields.Many2one('s_vehicule_marque', string='Marque')
    s_modele = fields.Many2one('s_vehicule_modele', string='Modèle')
    s_serie = fields.Many2one('s_vehicule_serie', string='Série')
