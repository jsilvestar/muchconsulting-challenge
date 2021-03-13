# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class ProjectStageMergeWizard(models.TransientModel):
    _name = 'project.stage.merge.wizard'
    _description = 'Project Stage Merge Wizard'

    merge_from_id = fields.Many2one(
    	'project.task.type',
        'Merge From', 
    	required=True
    )
    merge_to_id = fields.Many2one(
    	'project.task.type',
        'Merge To',
    	required=True
    )


    def action_project_stage_merge(self):
        """To merge project stage id.
			@param self: The object pointer.
			@param merge_from_id: From project.task.type id
			@param merge_to_id: To  project.task.type id
			@return: from_id will be merged into to project task type id
        """
        if self._context.get('active_ids'):
            active_ids = self._context.get('active_ids')
            project_task_ids = self.env['project.task'].search(
            	[('project_id', '=', active_ids), ('stage_id', '=', self.merge_from_id.id)])
            for task_id in project_task_ids:
            	task_id.write({
            		'stage_id': self.merge_to_id.id
            	})
