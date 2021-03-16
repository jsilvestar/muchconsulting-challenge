# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    base_parner_driver_id = fields.Char(string='Driver ID')
    nationality = fields.Char(string='Nationality')
    surname = fields.Char(string='Surname')
