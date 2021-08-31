# # -*- coding: utf-8 -*-
# from odoo import fields, models
#
#
# class StockMove(models.Model):
#     _inherit = 'stock.move'
#
#     s_mat_1 = fields.Many2one('product.product')
#     s_mat_2 = fields.Many2one('product.product')
#     s_placement_mat_1 = fields.Char()
#     s_placement_mat_2 = fields.Char()
#
#     def _prepare_procurement_values(self):
#         """ Prepare specific key for moves or other componenets that will be created from a stock rule
#         comming from a stock move. This method could be override in order to add other custom key that could
#         be used in move/po creation."""
#         self.ensure_one()
#         group_id = self.group_id or False
#         if self.rule_id:
#             if self.rule_id.group_propagation_option == 'fixed' and self.rule_id.group_id:
#                 group_id = self.rule_id.group_id
#             elif self.rule_id.group_propagation_option == 'none':
#                 group_id = False
#         return {
#             'date_planned': self.date_expected,
#             'move_dest_ids': self,
#             'group_id': group_id,
#             'route_ids': self.route_ids,
#             'warehouse_id': self.warehouse_id or self.picking_id.picking_type_id.warehouse_id or self.picking_type_id.warehouse_id,
#             'priority': self.priority,
#             's_mat_1': self.s_mat_1.id,
#             's_mat_2': self.s_mat_2.id,
#             's_placement_mat_1': self.s_placement_mat_1,
#             's_placement_mat_2': self.s_placement_mat_2,
#         }
