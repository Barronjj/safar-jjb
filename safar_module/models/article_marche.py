# -*- coding: utf-8 -*-
from odoo import models, fields


class Article_marche(models.Model):
    _name = 's_article_marche'
    _description = 'article_marche'
    _rec_name = 's_name'

    s_name = fields.Char(string='Nom')
