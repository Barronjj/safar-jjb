# -*- coding: utf-8 -*-
from odoo import models, fields


class DelaiFabrication(models.Model):
    _name = 's_delai_fabrication'
    _description = 'delai fabrication'
    _rec_name = 's_cd_delai'

    s_cd_delai = fields.Char(string='Famille délai fabrication')
    s_duree_jr = fields.Integer(string="Délai (jr)")

	# Si la durée en jour a été modifiée alors on la reporte sur tous les articles concernés
    def write(self, values):
        if 's_duree_jr' in values:
            list_art = self.env['product.template'].search([('s_cd_delai_fabrication', '=', self.id)])
            for art in list_art:
                art_vals = []
                art_vals = {
                    'sale_delay': values.get('s_duree_jr', 0),
                }

                if art_vals:
                    art.write(art_vals)

        return super(DelaiFabrication, self).write(values)