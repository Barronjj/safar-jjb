# -*- coding: utf-8 -*-
from odoo import fields, models, api


class MrpRoutingWorkcenter(models.Model):
    _inherit = 'mrp.routing.workcenter'
    s_uo_percent = fields.Integer(string="% UO")