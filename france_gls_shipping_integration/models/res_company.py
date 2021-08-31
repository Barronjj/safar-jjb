from odoo import models, fields,api
class ResCompany(models.Model):
    _inherit = "res.company"
    gls_username = fields.Char(string="GLS Username", help="GLS Username given by GLS.",copy=False)
    gls_password = fields.Char(copy=False,string='GLS Password', help="GLS Password given by GLS.")
    gls_api_url = fields.Char(copy=False,string='GLS API URL', help="API URL, Redirect to this URL when calling the API.",default="https://api-qs.gls-group.eu/public/v1")
    gls_customer_id = fields.Char(copy=False,string='GLS Customer ID', help="GLS Customer ID.")
    gls_contact_id = fields.Char(copy=False,string='GLS ContactID', help="GLS ContactID.")
    use_gls_fr_shipping_provider = fields.Boolean(copy=False, string="Are You Using GLS.?",
                                                 help="If use GLS shipping Integration than value set TRUE.",
                                                 default=False)

    def weight_convertion(self, weight_unit, weight):
        pound_for_kg = 2.20462
        ounce_for_kg = 35.274
        if weight_unit in ["LB", "LBS"]:
            return round(weight * pound_for_kg, 3)
        elif weight_unit in ["OZ", "OZS"]:
            return round(weight * ounce_for_kg, 3)
        else:
            return round(weight, 3)
