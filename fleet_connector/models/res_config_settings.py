# -*- coding: utf-8 -*-

import logging
import threading
import json
import requests

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    fleet_username = fields.Char(
        string='User Name',
        config_parameter='hr_fleet.fleet_username'
    )
    fleet_password = fields.Char(
        string='Password',
        config_parameter='hr_fleet.fleet_password'
    )

    def _import_fleet_partner(self, rec):
        """ This Thread will Import all Driver
        """
        with api.Environment.manage():
            # As this function is in a new thread, I need to open a new cursor, because the old one may be closed
            new_cr = self.pool.cursor()
            self = self.with_env(self.env(cr=new_cr))
            try:
                _logger.info('Attempt to run Import Fleet Driver')
                drivers = rec.get('drivers')
                for driver in drivers:
                    address = driver.get('address')
                    partner_country = address.get('country')
                    CountryObj = self.env['res.country']
                    StateObj = self.env['res.country.state']
                    country = CountryObj.search(
                        [('code', '=ilike', partner_country.get('country_code'))], limit=1)
                    if country:
                        country_id = country
                    else:
                        country_dict = ({
                            'name': partner_country.get('name'),
                            'code': partner_country.get('country_code')
                        })
                        country_id = CountryObj.sudo().create(country_dict)
                    partner_id = self.env['res.partner'].search(
                        [('base_parner_driver_id', '=', driver.get('id'))])
                    if not partner_id:
                        partner = {
                            'name': driver.get('name'),
                            'email': driver.get('email'),
                            'function': driver.get('email'),
                            'phone': driver.get('telephone'),
                            'base_parner_driver_id': driver.get('id'),
                            'nationality': driver.get('nationality'),
                            'surname': driver.get('surname'),
                            'street': address.get('street'),
                            'zip': address.get('zip'),
                            'city': address.get('city'),
                            'country_id': country_id.id,
                        }
                        partner_id = self.env['res.partner'].create(partner)
            except Exception:
                _logger.info(
                    'Attempt to run Import Fleet Partner aborted, as already running')
                self._cr.rollback()
                self._cr.close()
                return {}
            new_cr.commit()
            new_cr.close()
            return {}

    def _import_fleet_truck(self, rec):
        """This thread will be called after importing driver and this will map 
        driver and truck.
        """
        with api.Environment.manage():
            new_cr = self.pool.cursor()
            self = self.with_env(self.env(cr=new_cr))
            try:
                _logger.info('Attempt to run Import Trucks')
                trucks = rec.get('trucks')
                for truck in trucks:
                    first, last = truck.get('model').split()
                    FleetModelBrandObj = self.env['fleet.vehicle.model.brand']
                    model_brand = FleetModelBrandObj.search([('name', '=ilike', first.split('-')[0])])
                    if model_brand:
                        model_brand_id = model_brand
                    else:
                        truck_model = {
                            'name': first.split('-')[0],
                        }
                        model_brand_id = FleetModelBrandObj.sudo().create(truck_model)
                    FleetModelObj = self.env['fleet.vehicle.model']
                    FleetModelBrandObj = self.env['fleet.vehicle.model.brand']
                    model_brand = FleetModelBrandObj.search([('name', '=ilike', first.split('-')[0])])
                    fleet_model = FleetModelObj.search([('name', '=ilike', last),
                     ('brand_id', '=', model_brand_id.id)], limit=1)
                    if not fleet_model:
                        fleet_model_rec = {
                            'name': last,
                            'brand_id': model_brand_id.id
                        }
                        fleet_model_id = FleetModelObj.sudo().create(fleet_model_rec)
                    else:
                        fleet_model_id = fleet_model
                    partner_id = self.env['res.partner'].search(
                        [('base_parner_driver_id', '=', truck.get('driver_id'))], limit=1)
                    position = truck.get('position')
                    fleet_rec = {
                        'model_id': fleet_model_id.id,
                        'driver_id': partner_id.id,
                        'license_plate': truck.get('model'),
                        'base_driver_id': truck.get('driver_id'),
                        'base_fleet_id': truck.get('id'),
                        'base_truck_company': truck.get('company'),
                    }
                    fleet_vehicle = self.env['fleet.vehicle'].sudo().create(fleet_rec)
            except Exception:
                _logger.info(
                    'Attempt to run Import Fleet Trucks aborted, as already running')
                self._cr.rollback()
                self._cr.close()
                return {}
            new_cr.commit()
            new_cr.close()
            return {}

    def import_fleet(self):
        """ Calling Thread method to Import Driver and Truck
        """
        payload = {
            "username": self.env['ir.config_parameter'].sudo().get_param('hr_fleet.fleet_username', 'False'),
            "password": self.env['ir.config_parameter'].sudo().get_param('hr_fleet.fleet_password', 'False')
        }
        response = requests.post(
            "https://zp0xx3z3bi.execute-api.eu-central-1.amazonaws.com/prod/data",
            data=json.dumps(payload)
        )
        if response.status_code == requests.codes.ok:
            response = response.json()
        else:
            return {'error': response.status_code}
        threaded_partner = threading.Thread(
            target=self._import_fleet_partner, args=[response])
        threaded_truck = threading.Thread(
            target=self._import_fleet_truck, args=[response])
        threaded_partner.start()
        threaded_partner.join()
        threaded_truck.start()
        return True
