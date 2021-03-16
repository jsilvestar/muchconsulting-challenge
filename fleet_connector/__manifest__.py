# -*- coding: utf-8 -*-
{
    'name': "Fleet Connector",
    'description': """
        This Module allows to Import Driver and Truck Detils
        Trucks can be Tracked based on geo location
    """,
    'author': "MuchConsulting",
    'website': "http://www.muchconsulting.de",
    'category': 'Fleet',
    'version': '0.1',
    'depends': ['fleet', 'base_geolocalize'],
    'data': [
        'views/res_partner_views.xml',
        'views/fleet_views.xml',
        'views/res_config_settings_views.xml',
    ],
}
