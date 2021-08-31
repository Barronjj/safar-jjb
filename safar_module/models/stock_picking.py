# -*- coding: utf-8 -*-
from odoo import fields, models, api

import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def create(self, values):
        record = super(StockPicking, self).create(values)

        # on ajoute par défaut le transporteur GLS au BL
        _logger.critical("OK")
        company = self.env['res.company'].search([('id', '=', record.company_id.id)])
        if company:
            _logger.critical("COMPANY : " + str(company.id))
            if company.s_methode_expe_par_defaut:
                _logger.critical("CARRIER : " + str(company.s_methode_expe_par_defaut.id))
                record.carrier_id = company.s_methode_expe_par_defaut.id

        return record