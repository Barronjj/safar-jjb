# -*- coding: utf-8 -*-
from odoo import http


# class SafarModule(http.Controller):
#     @http.route('/safar_module/safar_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/safar_module/safar_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('safar_module.listing', {
#             'root': '/safar_module/safar_module',
#             'objects': http.request.env['safar_module.safar_module'].search([]),
#         })

#     @http.route('/safar_module/safar_module/objects/<model("safar_module.safar_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('safar_module.object', {
#             'object': obj
#         })
