# -*- coding: utf-8 -*-
from odoo import models, fields


class Vehicule_modele(models.Model):
    _name = 's_vehicule_modele'
    _description = 'vehicule_modele'
    _rec_name = 's_name'

    s_name = fields.Char(string="Nom")
    s_id_car_modele = fields.Integer(string='id_car_modele')
    s_marque = fields.Many2one('s_vehicule_marque', string='Marque')
    s_univers = fields.Many2one('s_vehicule_univers', string='Univers')
