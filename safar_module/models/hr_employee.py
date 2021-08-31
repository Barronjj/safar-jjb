from odoo import fields, models, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    s_cd_binome = fields.Char(string="Code Binôme")