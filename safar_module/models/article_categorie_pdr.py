# -*- coding: utf-8 -*-
from odoo import models, fields


class ArticleCategoriePdr(models.Model):
    _name = 's_article_categorie_pdr'
    _description = 'article_categorie_pdr'
    _rec_name = 's_name'

    s_name = fields.Char(string='Nom')