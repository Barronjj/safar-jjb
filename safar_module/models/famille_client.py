# -*- coding: utf-8 -*-
from odoo import models, fields, api


class FamilleClient(models.Model):
    _name = 's_famille_client'
    _description = 'famille_client'
    _rec_name = 's_display_name'

    s_name = fields.Char(string='Nom')
    s_display_name = fields.Char(compute='_compute_name', string='Famille client', search='pro_search', store="True")
    s_parent_id = fields.Many2one('s_famille_client', string="Famille mère")

    @api.depends('s_name', 's_parent_id')
    def _compute_name(self):
        for record in self:
            record.s_display_name = record.s_parent_id.__getattribute__('s_display_name') + " / " + record.s_name \
                if record.s_parent_id else record.s_name

    def pro_search(self, operator, value):
        if operator == 'like':
            operator = 'ilike'
            display_name = self.env['s_famille_client'].search([('s_display_name', operator, value)], limit=None)
        return [(display_name, operator, value)]

