# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FleetVechicle(models.Model):
    _inherit = 'fleet.vehicle'

    base_driver_id = fields.Char(string='Driver ID')
    base_fleet_id = fields.Char(string='Fleet ID')
    base_truck_company = fields.Char(string='Fleet Company')
    self_owned = fields.Boolean(string='Self Owned')
    registration = fields.Char(string='Registration')

    date_localization = fields.Date(string='Geolocation Date')
    driver_latitude = fields.Float(string='Latitude')
    driver_longitude = fields.Char(string='Longitude')


    @api.model
    def _geo_localize(self, street='', zip='', city='', state='', country=''):
        geo_obj = self.env['base.geocoder']
        search = geo_obj.geo_query_address(street=street, zip=zip, city=city, state=state, country=country)
        result = geo_obj.geo_find(search, force_country=country)
        if result is None:
            search = geo_obj.geo_query_address(city=city, state=state, country=country)
            result = geo_obj.geo_find(search, force_country=country)
        return result

    def geo_localize(self):
        """ Find Truck based on Provided geo location in the form.
        """
        # We need country names in English below
        for partner in self.with_context(lang='en_US'):
            result = self._geo_localize(self.driver_id.street,
                                        self.driver_id.zip,
                                        self.driver_id.city,
                                        self.driver_id.state_id.name,
                                        self.driver_id.country_id.name)

            if result:
                partner.write({
                    'driver_latitude': result[0],
                    'driver_longitude': result[1],
                    'date_localization': fields.Date.context_today(self.driver_id)
                })
        return True
            