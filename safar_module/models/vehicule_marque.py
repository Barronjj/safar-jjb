# -*- coding: utf-8 -*-
from odoo import models, fields


class Vehicule_marque(models.Model):
    _name = 's_vehicule_marque'
    _description = 'vehicule_marque'
    _rec_name = 's_name'

    s_name = fields.Char(string='Nom')
    s_code_court = fields.Char(string='Code court')
    s_id_car_make = fields.Integer(string='id car make')
