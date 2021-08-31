# -*- coding: utf-8 -*-
from odoo import models, fields, api

class GroupeClient(models.Model):
    _name = 's_groupe_client'
    _description = 'groupe_client'
    _rec_name = 's_name'

    s_name = fields.Char(string='Groupe client')
