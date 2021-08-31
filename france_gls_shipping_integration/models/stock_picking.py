from odoo import fields, models, api, _

class StockPickingVTS(models.Model):
    _inherit = 'stock.picking'
    gls_fr_tracking_url = fields.Char(string="GLS Tracking URL",help="Tracking URL.",copy=False)
