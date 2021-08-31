# -*- coding: utf-8 -*-
from odoo import models, fields

class PlacementOF(models.Model):
    _name = 's_placement_of'
    _description = 'placement_of'
    _rec_name = 's_nom_placement'

    s_gabarit = fields.Char(string='Gabarit')
    s_type = fields.Char(string='Type')
    s_qte = fields.Integer(string='Quantité')
    s_laize = fields.Integer(string='Laize')
    s_lettre = fields.Selection(selection=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E')], string='Lettre placement')
    s_metrage = fields.Float(string='Métrage')
    s_nb_epaisseur = fields.Integer(string='Nb d\'épaisseurs')
    s_nom_placement = fields.Char(string='Nom Placement')
    s_of_id = fields.Many2one('mrp.production', ondelete='cascade')
    s_matiere = fields.Many2one('product.product', string="Matière")