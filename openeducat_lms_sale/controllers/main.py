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
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug


PPG = 12  # Products Per Page
PPR = 4  # Products Per Row


class OpenEduCatLmsSale(OpenEduCatLms):

    @http.route()
    def enroll_course(self, course, **kwargs):
        if course.type == 'free':
            super(OpenEduCatLmsSale, self).enroll_course(course, **kwargs)
            return request.redirect('/my-courses')
        else:
            super(OpenEduCatLmsSale, self).enroll_course(course, **kwargs)
            enrollment = request.env['op.course.enrollment'].sudo().search([
                ('user_id', '=', request.env.user.id),
                ('course_id', '=', course.id)])
            enrollment.sudo().state = 'draft'
            order = request.website.sale_get_order(force_create=1)
            order._cart_update(product_id=course.product_id.id, add_qty=1)
            enrollment.sudo().order_id = order
            return request.redirect('/shop/cart')

    @http.route([
        '/courses',
        '/courses/page/<int:page>',
        '/courses/category/<model("op.course.category"):category>',
        '/courses/category/<model(\
        "op.course.category"):category>/page/<int:page>',
        '/courses/type/<string:price>',
    ], type='http', auth="public", website=True)
    def courses(self, search='', category=False, page=0, price=0, ppg=False, **post):
        print("insideeeeeee\n\n\n\n\n\n\n\n\n", price)
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
        if price == 'free':
            domain += [('type', '=', 'free')]
        if price == 'paid':
            domain += [('type', '=', 'paid')]
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
        print("all course\n\n\n\n\n\n", all_courses)
        course_category_ref = request.env['op.course.category']
        if category:
            categories = course_category_ref.sudo().search(
                [('parent_id', '=', category.id)])
        else:
            categories = course_category_ref.sudo().search(
                [('parent_id', '=', False)])
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
                'openeducat_core.group_op_faculty')
        }
        return request.render("openeducat_lms_sale.course", values)
