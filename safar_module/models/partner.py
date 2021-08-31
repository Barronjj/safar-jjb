# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import fields, models, api, _
from datetime import datetime

class Partner(models.Model):
    _inherit = 'res.partner'

    s_num_client = fields.Integer(string="N° client SAFAR", copy=False)
    s_nb_jr_expedition_max = fields.Integer(string="Nb Jours Maxi pour l'expédition")
    s_id_gescom = fields.Char(string="Identifiant Gescom")
    s_compte_sage = fields.Char(string="Cd Comptable Sage")
    s_id_client_facture = fields.Many2one('res.partner', string="Client Facturé")
    s_cd_sap = fields.Char(string="Cd Sap")
    s_cd_facturation = fields.Char(string="Cd Facturation")
    s_dt_envoi_doc = fields.Date(string="Dt Envoi Doc")
    s_dt_envoi_depliant = fields.Date(string="Dt Envoi Dépliant")
    s_fax = fields.Char(string="Fax")
    s_est_un_prospect = fields.Boolean(string="Est Un Prospect")
    s_id_famille_client = fields.Many2one('s_famille_client', string="Famille Client")
    s_facture_par_mail = fields.Boolean(string="Envoyer facture Par Mail")
    s_id_groupe_client = fields.Many2one('s_groupe_client', string="Groupe Client")

    s_dt_optin = fields.Date(string="Dt Optin")
    s_dt_optout = fields.Date(string="Dt Optout")
    s_status_client = fields.Selection(selection=[('actif', 'Actif'), ('inactif', 'Inactif')], string="Statut Client")
    s_gescom_ca_2018 = fields.Float(currency_field="s_currency_id", string="CA 2018")
    s_gescom_ca_2019 = fields.Float(currency_field="s_currency_id", string="CA 2019")
    s_mt_encours_client = fields.Float(currency_field="s_currency_id", string="Encours Client")
    s_code_concession = fields.Char(string='Code concession')
    s_nature_client = fields.Selection(selection=[('agent', 'Agent'), ('direct', 'Direct'), ('groupe', 'Groupe'),
                                                  ('importateur', 'Importateur'), ('reseau', 'Réseau')],
                                       string="Nature Client")

    s_id_structure_juridique = fields.Many2one('s_structure_juridique', string="Structure Juridique")
    s_tab_references_article = fields.One2many('s_produit_client', 's_client')

    s_currency_id = fields.Many2one('res.currency', string="Currency Id")

    s_info_marque = fields.Char(string="Info Marques")
    #s_mail_facturation = fields.Text(string="Courriel facturation")
    s_modif_date = fields.Datetime()
    s_modif_user = fields.Many2one('res.users')
    s_jr_facturation = fields.Selection(selection=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'),
                                                   ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'),
                                                   ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'),
                                                   ('29', '29'), ('30', '30'), ('31', '31')], string="Num Jour Facturation")
    s_rib_sur_facture = fields.Many2one('account.journal', string="RIB sur facture")

    @api.model
    def create(self, values):
        # Atribution du s_num_client : Max num_client +1
        record = super(Partner, self).create(values)
        record_num_client = self.env['res.partner'].search([('s_num_client', '!=', False)], order='s_num_client desc', limit=1)
        if values.get('s_num_client'):
            record['s_num_client'] = values.get('s_num_client')
        else:
            record['s_num_client'] = str(max(60000, int(record_num_client.s_num_client)+1))

        # On récupère la currency EUR pour le widget monetary
        currency = self.env['res.currency'].search([('id', '=', '1')], limit=1)
        record['s_currency_id'] = currency
        return record

    def write(self, values):
        # on cherche le user en cours
        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)

        if self.env.uid != 1:
            # si ce n'est pas OdooBot, alors on enregistre le user et la date de modif
            values['s_modif_user'] = self.env.uid #user.id
            values['s_modif_date'] = datetime.now()

        return super(Partner, self).write(values)

    def call_safar_config_partner(self):
        """Ouvre le configurateur SAFAR dans une nouvelle fenetre"""
        url_site = self.env['ir.config_parameter'].get_param('url.configurateur')
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': url_site + '?client="' + str(self.s_num_client) + '"',
            # 'url': 'http://jjbconseil.wd25.francelink.net/SAFAR_Configurateur?client="' + str(self.s_num_client) + '"',
        }

    def name_get(self):
        """Méthode permettant de changer la donnée affichée dans certains Many2one"""
        ret = []
        origin = super(Partner, self).name_get()
        for record in self:
            if record._context.get('show_code_concession', False):
                if record.s_code_concession:
                    ret.append((record.id, str(record.s_code_concession) + " - " + str(record.name)))
                else:
                    ret.append((record.id, str(record.name)))
            elif record._context.get('partner_livraison_adr', False):
                if record.city and record.s_code_concession:
                    ret.append((record.id, str(record.name) + " - " + str(record.s_code_concession) + " - " + str(record.city) + ", " + str(record.street)))
                elif record.city:
                    ret.append((record.id, str(record.name) + " - " + str(record.city) + ", " + str(record.street)))
                elif record.s_code_concession:
                    ret.append((record.id, str(record.name) + " - " + str(record.s_code_concession)))
                else:
                    ret.append((record.id, str(record.name) + " - " + str(record.street)))
            else:
                return origin
        return ret

    @api.depends('s_info_marque', 's_status_client', 'company_id', 'parent_id', 'state', 'date_order')
    def check_partner_actif(self):
        limit_dt = fields.Date.today() + relativedelta(years=-2)
        partners = self.env['res.partner'].search([('company_id', '=', False), ('parent_id', '=', False)])
        # pour chaque client qui peut commander, donc sans parent...
        for partner in partners:
            if not partner.s_status_client:
                partner.s_status_client = 'inactif'

            # ...on cherche quelle est sa dernière commande
            last_cde = self.env['sale.order'].search([('partner_id', '=', partner.id), '|', ('state', '=', 'sale'), ('state', '=', 'done')], order="date_order desc", limit=1)
            # ...et on regarde si elle a plus de 2 ans
            if last_cde:
                if last_cde.date_order.date() > limit_dt:
                    if partner.s_status_client != 'actif':
                        partner.s_status_client = 'actif'
                else:
                    if partner.s_status_client != 'inactif':
                        partner.s_status_client = 'inactif'

    @api.onchange('parent_id')
    def onchange_parent_id(self):
        # return values in result, as this method is used by _fields_sync()
        # surcharge de la méthode Odoo pour éviter de modifier l'adresse lorsque le contact ETAIT contact (cas d'un changement de type)
        if not self.parent_id:
            return
        result = {}
        partner = self._origin
        if partner.parent_id and partner.parent_id != self.parent_id:
            result['warning'] = {
                    'title': _('Warning'),
        'message': _('Changing the company of a contact should only be done if it '
                                 'was never correctly set. If an existing contact starts working for a new '
                                 'company then a new contact should be created under that new '
                                 'company. You can use the "Discard" button to abandon this change.')}
        if self.type == 'contact':
            # for contacts: copy the parent address, if set (aka, at least one
            # value is set in the address: otherwise, keep the one from the
            # contact)
            address_fields = self._address_fields()
            if any(self.parent_id[key] for key in address_fields):
                def convert(value):
                    return value.id if isinstance(value, models.BaseModel) else value
                result['value'] = {key: convert(self.parent_id[key]) for key in address_fields}
        return result