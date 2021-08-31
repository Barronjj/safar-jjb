# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    s_code_concession = fields.Many2one('res.partner', string="Code concession de")
    s_code_concession_related = fields.Char(related="s_code_concession.s_code_concession", store="True", string="Code concession lié")
    # s_id_client_facture = fields.Integer(related="partner_invoice_id.id", store="True",
    #                                      string="Id client facture")
    s_client_facture_related = fields.Char(related="partner_invoice_id.name", store="false")
    s_interlocuteur = fields.Many2one('res.partner', string="Interlocuteur")
    s_interlocuteur_email = fields.Char(related="s_interlocuteur.email")
    s_configuration_exist = fields.Boolean(compute="compute_configuration_existe", store="True", string="Présence d'une config dans la cde")
    s_no_ligne_commande_exist = fields.Boolean(compute="compute_no_ligne_commande_existe", store="True", string="Présence d'un n° de ligne dans la cde")
    s_num_clt_facture_related = fields.Integer(related="partner_invoice_id.s_num_client", store="False")
    s_jr_facturation_related = fields.Selection(related="partner_invoice_id.s_jr_facturation", store="False", string="Num Jr Facturation")

    """CODE récupéré depuis application achetée sur le store 'Sale order quick MRP information'"""
    sh_mrp_ids = fields.Many2many(
        comodel_name='mrp.production',
        string="Ordre de fabrication",
        compute='_compute_mrp_orders'
    )

    mrp_count = fields.Integer(
        string="Ordres de fabrication",
        compute='_compute_mrp_count'
    )
    """Fin du code acheté"""

    @api.onchange('partner_shipping_id')
    def onchange_partner_shipping_id(self):
        if self.partner_shipping_id.s_code_concession:
            self.s_code_concession = self.partner_shipping_id if self.partner_shipping_id else self.partner_id
        else:
            self.s_code_concession = self.partner_id if self.partner_id else False

    @api.onchange('partner_invoice_id')
    def onchange_partner_invoice_id(self):
        """search = self.env['res.partner'].search(['&', ('s_id_client_facture', '=', self.partner_invoice_id.id),
                                                 ('id', 'child_of', self.partner_id.id)],
                                                limit=1)
        self.s_code_concession = search if search else self.partner_invoice_id"""
        self.payment_term_id = self.partner_invoice_id.s_id_client_facture.property_payment_term_id \
            if self.partner_invoice_id.s_id_client_facture.property_payment_term_id \
            else self.partner_invoice_id.property_payment_term_id
        self.pricelist_id = self.partner_invoice_id.s_id_client_facture.property_product_pricelist \
            if self.partner_invoice_id.s_id_client_facture.property_product_pricelist \
            else self.partner_invoice_id.property_product_pricelist
        self.fiscal_position_id = self.partner_invoice_id.s_id_client_facture.property_account_position_id \
            if self.partner_invoice_id.s_id_client_facture.property_account_position_id \
            else self.partner_invoice_id.property_account_position_id

    @api.onchange('s_code_concession')
    def onchange_s_code_concession(self):
        self.partner_invoice_id = self.s_code_concession.s_id_client_facture \
            if self.s_code_concession.s_id_client_facture \
            else self.s_code_concession

    """Overide the function to add s_code_concession and change partner_invoice_id base value"""
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        # res = super(SaleOrder, self).onchange_partner_id()
        """
        Update the following fields when the partner is changed:
        - Pricelist
        - Payment terms
        - Invoice address
        - Delivery address
        - Code concession
        """
        if not self.partner_id:
            self.update({
                'payment_term_id': False,
                'partner_invoice_id': False,
                'partner_shipping_id': False,
                'fiscal_position_id': False,
                's_code_concession': False,
            })
            return

        addr = self.partner_id.address_get(['delivery', 'invoice', 'contact'])
        partner_user = self.partner_id.user_id or self.partner_id.commercial_partner_id.user_id
        values = {
            # 'pricelist_id': self.partner_invoice_id.property_product_pricelist or self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
            # 'pricelist_id': self.partner_id.s_id_client_facture.property_product_pricelist
            # if self.partner_id.s_id_client_facture.property_product_pricelist
            # else self.partner_id.property_product_pricelist,
            # 'payment_term_id': self.partner_id.s_id_client_facture.property_payment_term_id
            # if self.partner_id.s_id_client_facture.property_payment_term_id
            # else self.partner_id.property_payment_term_id,
            # 'partner_invoice_id': self.partner_id.s_id_client_facture if self.partner_id.s_id_client_facture else addr['invoice'],
            # 'partner_shipping_id': addr['delivery'],
            # 's_code_concession': self.partner_id,
            'partner_shipping_id': addr['contact'],
            # 's_code_concession': self.partner_shipping_id if self.partner_shipping_id else False,
            'payment_term_id':
                self.partner_invoice_id.property_payment_term_id if
                self.partner_invoice_id.property_payment_term_id else
                self.partner_id.property_payment_term_id,
        }
        user_id = partner_user.id or self.env.uid
        if self.user_id.id != user_id:
            values['user_id'] = user_id

        if self.env['ir.config_parameter'].sudo().get_param('account.use_invoice_terms') and self.env.company.invoice_terms:
            values['note'] = self.with_context(lang=self.partner_id.lang).env.company.invoice_terms

        values['team_id'] = self.env['crm.team']._get_default_team_id(user_id=user_id)
        self.update(values)

    """Ouvre le configurateur SAFAR dans une nouvelle fenetre"""
    def call_safar_config_saleorder(self):
        url_site = self.env['ir.config_parameter'].get_param('url.configurateur')
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': url_site + '?client="' +
                   str(self.partner_id.s_num_client) + '"&invoiceId="' + str(self.id) + '"',
        }

    """Ouvre une vue modale (wizzard) pour rechercher un product dans une pricelist"""
    def open_search_item_pricelist_view(self):
        for order in self:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Chercher un produit par sa référence client',
                'res_model': 'product.pricelist',
                'view_type': 'tree',
                'view_mode': 'tree',
                'res_id': order.pricelist_id,
                'view_id': self.env.ref('safar_module.s_product_pricelist_item_tree_view', False).id,
                'target': 'new',
            }

    """Vérifie dans toutes les lignes de la cde, si il y a au moins une configuration de renseignée"""
    @api.depends('order_line', 'order_line.s_configuration')
    def compute_configuration_existe(self):
        for record in self:
            configuration_exist = False
            for line in record.order_line:
                if line.s_configuration:
                    configuration_exist = True
                    break

            record.update({'s_configuration_exist': configuration_exist})

    """Vérifie dans toutes les lignes de la cde, si il y a au moins un numéro de ligne de renseigné"""
    @api.depends('order_line', 'order_line.s_no_ligne_commande')
    def compute_no_ligne_commande_existe(self):
        for record in self:
            no_ligne_cde_exist = False
            for line in record.order_line:
                if line.s_no_ligne_commande:
                    no_ligne_cde_exist = True
                    break

            record.update({'s_no_ligne_commande_exist': no_ligne_cde_exist})

            # def action_view_of(self):
    #     invoices = self.mapped('invoice_ids')
    #     action = self.env.ref('account.action_move_out_invoice_type').read()[0]
    #     if len(invoices) > 1:
    #         action['domain'] = [('id', 'in', invoices.ids)]
    #     elif len(invoices) == 1:
    #         form_view = [(self.env.ref('account.view_move_form').id,'form')]
    #         if 'views' in action:
    #             action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
    #         else:
    #             action['views'] = form_view
    #         action['res_id'] = invoices.id
    #     else:
    #         action = {'type': 'ir.actions.act_window_close'}
    #
    #     context = {
    #         'default_type': 'out_invoice',
    #     }
    #     if len(self) == 1:
    #         context.update({
    #             'default_partner_id': self.partner_id.id,
    #             'default_partner_shipping_id': self.partner_shipping_id.id,
    #             'default_invoice_payment_term_id': self.payment_term_id.id or self.partner_id.property_payment_term_id.id or
    #                 self.env['account.move'].default_get(['invoice_payment_term_id']).get('invoice_payment_term_id'),
    #             'default_invoice_origin': self.mapped('name'),
    #             'default_user_id': self.user_id.id,
    #         })
    #     action['context'] = context
    #     return action

    """CODE récupéré depuis application achetée sur le store 'Sale order quick MRP information'"""
    def _compute_mrp_count(self):
        if self:
            for rec in self:
                mrp_orders = self.env['mrp.production'].sudo().search([
                    ('origin', '=', rec.name)
                ])
                if mrp_orders:
                    rec.mrp_count = len(mrp_orders.ids)
                else:
                    rec.mrp_count = 0

    def action_view_manufacturing(self):
        return {
            'name': 'Manufacturing Orders',
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.production',
            'view_mode': 'tree,form',
            'domain': [('origin', '=', self.name)],
            'target': 'current'
        }

    def _compute_mrp_orders(self):
        if self:
            for rec in self:
                mrp_orders = self.env['mrp.production'].sudo().search([
                    ('origin', '=', rec.name)
                ])
                if mrp_orders:
                    rec.sh_mrp_ids = [(6, 0, mrp_orders.ids)]
                else:
                    rec.sh_mrp_ids = False

    """Fin du code acheté"""