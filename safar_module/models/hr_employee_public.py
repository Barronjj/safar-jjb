from odoo import fields, models, api


class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    s_cd_binome = fields.Char(string="Code Binôme")