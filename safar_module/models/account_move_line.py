# -*- coding: utf-8 -*-
from odoo import fields, models, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    s_init_client = fields.Many2one('res.partner', string="Init Client")

    s_bl_id = fields.Integer(compute='_compute_bl', store="true", string="Id BL")
    s_bl_name = fields.Char()
    s_bl_date = fields.Date()

    s_cde_id = fields.Integer() #compute='_compute_cde', store="true", string="Id Cde")
    s_cde_name = fields.Char()
    s_cde_line_id = fields.Integer()
    s_cde_date = fields.Date()
    s_no_ligne_commande = fields.Char(string="N° ligne")
    s_ref_order_client = fields.Char()
    s_code_concession = fields.Char()

    s_ref_client = fields.Char() #compute='_compute_ref_client_account', store="True", string="Réf. article pour le client")
    s_tri_invoice_line = fields.Integer(compute="_compute_order_invoice_line_by_idcde", strore="false")

    # Permet de mettre un entier selon qu'il y a présence d'un id de cde ou pas pour le tri lors de l'impression
    # le but étant de distinguer les lignes ajoutées dans la facture (section, note) afin qu'elles apparaissent en premier dans les lignes
    # au-dessus des lignes issues de cde
    # on ne fait pas directement le tri sur l'id de cde car les lignes issues de cde ne doivent pas être triées sur cet id
    def _compute_order_invoice_line_by_idcde(self):  # self = ligne d'une facture
        for record in self:
            if record.s_cde_id > 0:
                record.s_tri_invoice_line = 3
            else:
                if record.display_type == 'line_section':
                    record.s_tri_invoice_line = 0
                elif record.display_type == 'line_note':
                    record.s_tri_invoice_line = 1
                else:
                    record.s_tri_invoice_line = 2

    # @api.depends('sale_line_ids')
    # def _compute_cde(self):  #self = ligne d'une facture
    #     for record in self:
    #         id_cde = 0
    #         nm_cde = ''
    #         dt_cde = ''
    #         id_line_cde = 0
    #         ref_order_clt = ''
    #         num_line = ''
    #         cd_concession = ''
    #         for ref in record.sale_line_ids:  # = sale.order.line
    #             id_cde = ref.order_id
    #             nm_cde = ref.order_id.name
    #             dt_cde = ref.order_id.date_order
    #             id_line_cde = ref.id
    #             num_line = ref.s_no_ligne_commande
    #             ref_order_clt = ref.order_id.client_order_ref
    #             cd_concession = ref.order_id.partner_id.s_code_concession
    #
    #         record.s_cde_id = id_cde
    #         record.s_cde_name = nm_cde
    #         record.s_cde_date = dt_cde
    #         record.s_cde_line_id = id_line_cde
    #         record.s_no_ligne_commande = num_line
    #         record.s_ref_order_client = ref_order_clt
    #         record.s_code_concession = cd_concession

    @api.depends('sale_line_ids')
    def _compute_bl(self): #self = ligne d'une facture
        for record in self:
            id_bl = ''
            name_bl = ''
            date_bl = ''

            records_move = self.env['stock.move'].search([('sale_line_id', 'in', record.sale_line_ids.ids)])
            for move in records_move:
                id_bl = move.picking_id.id
                name_bl = move.picking_id.name
                date_bl = move.picking_id.date_done

            record.s_bl_id = id_bl
            record.s_bl_name = name_bl
            record.s_bl_date = date_bl


    # @api.depends('sale_line_ids','product_id')
    # def _compute_ref_client_account(self): #self = ligne d'une facture
    #
    #         cd = ''
    #         prdt_id = 0
    #         for record in self:
    #             for order_line in record.sale_line_ids: #pour chaque ligne de cde de la ligne de facture (normalement 1 seule)
    #                 cd = order_line.s_ref_client
    #                 prdt_id = order_line.product_id
    #
    #             record.s_ref_client = cd if record.product_id == prdt_id else ''
