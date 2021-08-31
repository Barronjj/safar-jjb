# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Vehicule(models.Model):
    _name = 's_vehicule'
    _description = 'vehicule'
    _rec_name = 's_name'

    s_name = fields.Char(compute='_compute_name', search='pro_search', store="True", string="Nom")
    s_finition = fields.Many2one('s_vehicule_finition', string="Finition")
    s_generation = fields.Many2one('s_vehicule_generation', string="Génération")
    s_marque = fields.Many2one('s_vehicule_marque', string="Marque")
    s_modele = fields.Many2one('s_vehicule_modele', string="Modèle")
    s_serie = fields.Many2one('s_vehicule_serie', string="Série")
    s_gabarits = fields.One2many('s_vehicule_gabarit', 's_vehicule', string="Gabarits")

    @api.depends('s_finition', 's_generation', 's_marque', 's_modele', 's_serie')
    def _compute_name(self):
        for record in self:
            print(record.s_finition)
            print(record.s_finition.__getattribute__('s_name') if record.s_finition else "Bibop")
            if record.s_marque.__getattribute__('s_name'):
                record.s_name = record.s_marque.__getattribute__('s_name')
                if record.s_modele.__getattribute__('s_name'):
                    record.s_name = record.s_name + " " + record.s_modele.__getattribute__('s_name')
                    if record.s_generation.__getattribute__('s_name'):
                        record.s_name = record.s_name + " " + record.s_generation.__getattribute__('s_name')
                        if record.s_serie.__getattribute__('s_name'):
                            record.s_name = record.s_name + " " + record.s_serie.__getattribute__('s_name')
                            if record.s_finition.__getattribute__('s_name'):
                                record.s_name = record.s_name + " " + record.s_finition.__getattribute__('s_name')
            else:
                record.s_name = ""

    def pro_search(self, operator, value):
        if operator == 'like':
            operator = 'ilike'
            name = self.env['s_vehicule'].search([('s_name', operator, value)], limit=None)
        return [(name, operator, value)]

    @api.model
    def create(self, values):
        """Override default Odoo create function and extend."""
        # Do your custom logic here
        record_modeles = self.env['s_vehicule_modele'].search([('id', '=', values['s_modele'])])
        for record in record_modeles:
            record.write({
                's_marque': values['s_marque']
            })
        record_s_generation = self.env['s_vehicule_generation'].search([('id', '=', values['s_generation'])])
        for record in record_s_generation:
            record.write({
                's_marque': values['s_marque'],
                's_modele': values['s_modele']

            })
        record_s_serie = self.env['s_vehicule_serie'].search([('id', '=', values['s_serie'])])
        for record in record_s_serie:
            record.write({
                's_marque': values['s_marque'],
                's_modele': values['s_modele'],
                's_generation': values['s_generation']
            })
        record_s_finition = self.env['s_vehicule_finition'].search([('id', '=', values['s_finition'])])
        for record in record_s_finition:
            record.write({
                's_marque': values['s_marque'],
                's_modele': values['s_modele'],
                's_generation': values['s_generation'],
                's_serie': values['s_serie']
            })
        return super(Vehicule, self).create(values)

    def write(self, values):
        """Override default Odoo write function and extend."""
        # Do your custom logic here
        record_modeles = self.env['s_vehicule_modele'].search([('id', '=', values['s_modele'])]) \
            if 's_modele' in values \
            else self.env['s_vehicule_modele'].search([('id', '=', self.s_modele.__getattribute__('id'))])
        for record in record_modeles:
            record.write({
                's_marque': values['s_marque'] if 's_marque' in values else self.s_marque.__getattribute__('id')
            })
        record_s_generation = self.env['s_vehicule_generation'].search([('id', '=', values['s_generation'])]) \
            if 's_generation' in values \
            else self.env['s_vehicule_generation'].search([('id', '=', self.s_generation.__getattribute__('id'))])
        for record in record_s_generation:
            record.write({
                's_marque': values['s_marque'] if 's_marque' in values else self.s_marque.__getattribute__('id'),
                's_modele': values['s_modele'] if 's_modele' in values else self.s_modele.__getattribute__('id')

            })
        record_s_serie = self.env['s_vehicule_serie'].search([('id', '=', values['s_serie'])]) \
            if 's_serie' in values \
            else self.env['s_vehicule_serie'].search([('id', '=', self.s_serie.__getattribute__('id'))])
        for record in record_s_serie:
            record.write({
                's_marque': values['s_marque'] if 's_marque' in values else self.s_marque.__getattribute__('id'),
                's_modele': values['s_modele'] if 's_modele' in values else self.s_modele.__getattribute__('id'),
                's_generation': values['s_generation'] if 's_generation' in values else self.s_generation.__getattribute__('id')
            })
        record_s_finition = self.env['s_vehicule_finition'].search([('id', '=', values['s_finition'])]) \
            if 's_finition' in values \
            else self.env['s_vehicule_finition'].search([('id', '=', self.s_finition.__getattribute__('id'))])
        for record in record_s_finition:
            record.write({
                's_marque': values['s_marque'] if 's_marque' in values else self.s_marque.__getattribute__('id'),
                's_modele': values['s_modele'] if 's_modele' in values else self.s_modele.__getattribute__('id'),
                's_generation': values['s_generation'] if 's_generation' in values else self.s_generation.__getattribute__('id'),
                's_serie': values['s_serie'] if 's_serie' in values else self.s_serie.__getattribute__('id')
            })
        return super(Vehicule, self).write(values)
