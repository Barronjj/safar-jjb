# -*- coding: utf-8 -*-
from odoo import fields, models, api


class QualityCheck(models.Model):
    _inherit = 'quality.check'

    s_operateur = fields.Many2one('hr.employee', string="opérateur")
    s_note_operateur = fields.Text(string="Notes opérateur")