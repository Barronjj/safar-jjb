# -*- coding: utf-8 -*-
from odoo import models, fields


class StructureJuridique(models.Model):
    _name = 's_structure_juridique'
    _description = 'structure juridique'
    _rec_name = 's_name'

    s_name = fields.Char(string="Nom")
