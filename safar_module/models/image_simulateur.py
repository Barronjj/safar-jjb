# -*- coding: utf-8 -*-
from odoo import models, fields


class ImageSimulateur(models.Model):
    _name = 's_image_simulateur'
    _description = 'image simulateur'
    _rec_name = 's_name'

    s_name = fields.Char(string='Nom')
    s_image = fields.Binary(string="Image")
    s_univers = fields.Char(string="Univers")
    s_ref_pc = fields.Char(string="Ref. PC")
    s_ref_acc = fields.Char(string="Ref. ACC")
    s_type_vue = fields.Selection(selection=[('fac', 'Face'), ('cot', 'Côté'), ('aut', 'Autre')], string="Type Vue")