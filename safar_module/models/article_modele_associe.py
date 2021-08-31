# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ModeleAssocie(models.Model):
    _name = 's_article_modele_associe'
    _description = 'article_modele_associe'
    _rec_name = 's_name'

    s_name = fields.Char(string='Modèles associés')