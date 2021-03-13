# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    def open_tasks(self):
    	""" Based on a created project, the standard column would
    	be updated into prject.
        """
    	res = super(ProjectProject, self).open_tasks()
    	ctx = res.get('context')
    	project_id = ctx.get('search_default_project_id')
    	project_type_ids = self.env['project.task.type'].search([])
    	for project_type in project_type_ids:
    		project_type.update({'project_ids': [(4, project_id)]})
    	return res
            
