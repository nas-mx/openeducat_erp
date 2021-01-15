# -*- coding: utf-8 -*-
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech Receptives(<http://www.techreceptives.com>).
#
##############################################################################

from odoo import models, fields


class OpCourse(models.Model):
    _name = "op.course"
    _inherit = "op.course"

    survey_ids = fields.One2many('survey.survey', 'course_id', string='Survey')

    def get_survey(self):
        action = self.env.ref('survey.action_survey_form').read()[0]
        return action
