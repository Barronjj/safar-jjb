# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
from datetime import datetime


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    s_rib_par_defaut = fields.Boolean(string="RIB par défaut")