from odoo import fields, models, api


class Company(models.Model):
    _inherit = 'res.company'

    s_lib_capital_ste = fields.Char(string="Capital")
    s_logo_certificat = fields.Binary()
    s_tel_cde_devis = fields.Char(string="Tél Devis,Cde,BL,Proforma")
    s_email_cde_devis = fields.Char(string="Email Devis,Cde,BL,Proforma")
    s_tel_facture = fields.Char(string="Tél Facture,NC")
    s_email_facture = fields.Char(string="Email Facture,NC")
    s_methode_expe_par_defaut = fields.Many2one('delivery.carrier', string="Méthode par défaut")