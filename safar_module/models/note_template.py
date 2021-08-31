# -*- coding: utf-8 -*-
from odoo import models, fields

class NoteTemplate(models.Model):
    _name = 's_note_template'
    _description = 'note_template'
    _rec_name = 's_titre'

    s_name = fields.Text(string='Modèle de note')
    s_titre = fields.Char(String='Titre')