# -*- coding: utf-8 -*-
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech Receptives(<http://www.techreceptives.com>).
#
##############################################################################

from odoo import http
from odoo.addons.openeducat_lms.controllers.main import OpenEduCatLms
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug

PPG = 12  # Products Per Page
PPR = 4  # Products Per Row


class GamificationOpenEduCatLms(OpenEduCatLms):

    @http.route()
    def courses(self, search='', category=False, page=0, ppg=False, **post):
        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG
        domain = [('online_course', '=', True)]
        url = "/courses"
        if search:
            post["search"] = search
            for srch in search.split(" "):
                domain += [('name', 'ilike', srch)]
        if category:
            url = "/courses/category/%s" % slug(category)
            domain += [('category_ids', 'in', [category.id])]
        course_domain = domain + [
            ('visibility', 'in', ['public', 'logged_user']),
            ('state', '=', 'open')]
        course_ref = request.env['op.course']
        courses = course_ref.sudo().search(course_domain)
        invited_domain = domain + [
            ('invited_users_ids', 'in', [request.env.uid]),
            ('state', '=', 'open')]
        invited_courses = course_ref.sudo().search(invited_domain)
        total_count = len(courses) + len(invited_courses)
        pager = request.website.pager(
            url=url, total=total_count, page=page, step=ppg, scope=7,
            url_args=post)
        all_course_ids = [x.id for x in courses]
        all_course_ids += [x.id for x in invited_courses]
        all_courses = course_ref.sudo().search(
            [('id', 'in', all_course_ids)], limit=ppg, offset=pager['offset'])
        course_category_ref = request.env['op.course.category']
        if category:
            categories = course_category_ref.sudo().search(
                [('parent_id', '=', category.id)])
        else:
            categories = course_category_ref.sudo().search(
                [('parent_id', '=', False)])

        achievements = request.env['gamification.badge.user'].sudo().search(
            [('badge_id.is_published', '=', True)], limit=5)
        users = request.env['res.users'].sudo().search([
            ('karma', '>', 0),
            ('website_published', '=', True)], limit=5, order='karma desc')
        res = request.render('openeducat_lms_gamification.my_challenges')

        values = {
            'search': search,
            'pager': pager,
            'search_count': total_count,
            'courses': all_courses,
            'category': category,
            'categories': categories,
            'rows': 3,
            'user': request.env.user,
            'is_instructor': request.env.user.has_group(
                'openeducat_core.group_op_faculty'),
            'rr': res,
            'achievements': achievements,
            'users': users,
            'top3_users': self._get_top3_users()
        }
        return request.render("openeducat_lms.courses", values)

    def _get_top3_users(self):
        return request.env['res.users'].sudo().search_read([
            ('karma', '>', 0),
            ('website_published', '=', True),
            ('image_1920', '!=', False)], ['id'], limit=3, order='karma desc')

    @http.route()
    def enroll_course(self, course, **kwargs):
        r = super(GamificationOpenEduCatLms, self).enroll_course(
            course, **kwargs)
        course._action_set_course_done()
        for challenge in course.challenge_ids:

            current_challenge_users = challenge.user_ids.ids
            if request.env.uid not in current_challenge_users:
                current_challenge_users.append(request.env.uid)
                challenge.sudo().user_ids = [(6, 0, current_challenge_users)]
            challenge.sudo().action_start()
        return r

    @http.route()
    def get_course_material(self, course, section=None, material=None,
                            result=None, next_mat=None, **kwargs):
        r = super(GamificationOpenEduCatLms, self).get_course_material(
            course, section, material, result, next_mat, **kwargs)
        for challenge in course.challenge_ids:
            request.env['gamification.goal'].sudo().search(
                [('challenge_id', '=', challenge.id),
                 ('user_id', '=', request.env.uid),
                 ('state', '!=', 'reached')]).sudo().update_goal()
            challenge.sudo()._check_challenge_reward()
        reward = request.render('openeducat_lms_gamification.reward_point_view')
        r.qcontext.update({'reward': reward})
        reward_material = request.env['op.material'].sudo().search([
            ('material_type', '=', 'quiz')])

        if result:
            reward_material._action_set_quiz_material_done()
        return r

    @http.route(['/my/badges'], type='http', auth='public', website=True)
    def my_lms_badges(self, **post):
        badge_ids = request.env['gamification.badge.user'].search(
            [('user_id', '=', request.env.uid)])
        data = {'user': request.env.user}
        data['badge_ids'] = [x.badge_id for x in badge_ids]
        return request.render("openeducat_lms_gamification.my_badges", data)


class CustomerPortal(CustomerPortal):

    @http.route()
    def home(self, **kw):
        """ Add sales documents to main account page """
        response = super(CustomerPortal, self).home(**kw)
        badge_count = request.env[
            'gamification.badge.user'].sudo().search_count(
            [('user_id', '=', request.env.uid)])
        response.qcontext.update({
            'badge_count': badge_count
        })
        return response
