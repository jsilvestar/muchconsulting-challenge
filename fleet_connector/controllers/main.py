# -*- coding: utf-8 -*-
# from odoo import http


# class Learning(http.Controller):
#     @http.route('/learning/learning/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/learning/learning/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('learning.listing', {
#             'root': '/learning/learning',
#             'objects': http.request.env['learning.learning'].search([]),
#         })

#     @http.route('/learning/learning/objects/<model("learning.learning"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('learning.object', {
#             'object': obj
#         })
