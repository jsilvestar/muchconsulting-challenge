# -*- coding: utf-8 -*-
{
    'name': "Standard Prjoect",
    'description': """
        standardize the Projects kanban view. 
        and this module allows us to merge column with ease.
    """,
    'author': "MuchConsulting",
    'website': "http://www.muchconsulting.de",
    'category': 'project',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['project'],
    # always loaded
    'data': [
        'data/project_data.xml',
        'wizard/project_stage_merge_view.xml'
    ],
}
