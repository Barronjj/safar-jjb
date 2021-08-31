# -*- coding: utf-8 -*-
from odoo import models, fields


class Vehicule_univers(models.Model):
    _name = 's_vehicule_univers'
    _description = 'vehicule_univers'
    _rec_name = 's_name'

    s_name = fields.Char(string="Nom")
