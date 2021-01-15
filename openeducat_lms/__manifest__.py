# -*- coding: utf-8 -*-
# Part of OpenEduCat. See LICENSE file for full copyright & licensing details.
#
##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech Receptives(<http://www.techreceptives.com>).
#
##############################################################################


{
    'name': 'OpenEduCat LMS',
    'version': '13.0',
    'category': 'Education',
    "sequence": 3,
    'summary': 'LMS',
    'complexity': "easy",
    'author': 'Tech Receptives',
    'website': 'http://www.openeducat.org',
    'depends': [
        'portal',
        'website_mail',
        'website_rating',
        'auth_signup',
        'openeducat_core',
        'openeducat_quiz',
    ],
    'data': [
        'security/op_security.xml',
        'security/ir.model.access.csv',
        'views/assets.xml',
        'wizard/course_invitation_view.xml',
        'data/course_invitation.xml',
        'data/material_reminder.xml',
        'data/auth_signup.xml',
        'data/report_paperformat.xml',
        'data/certificate_sequence.xml',
        'views/quiz_view.xml',
        'views/course_catagory_view.xml',
        'views/op_level.xml',
        'views/course_view.xml',
        'views/faculty_view.xml',
        'views/course_detail.xml',
        'views/course_material.xml',
        'views/course_enrollment_view.xml',
        'views/website_lms.xml',
        'views/lms_embed.xml',
        'views/material_detail_view.xml',
        'views/my_courses.xml',
        'views/lms_onboard.xml',
        'views/certificate_portal.xml',
        'views/course_section_view.xml',
        'views/course_section_material_view.xml',
        'reports/course_reports.xml',
        'reports/course_certificate_templates.xml',
        'dashboard/lms_dashboard.xml',
        'menus/op_menu.xml',
    ],
    'demo': [
        'demo/op_level_data.xml',
        'demo/op_course_category_data.xml',
        'demo/op_material_data.xml',
        'demo/op_course_data.xml',
        'demo/op_course_section_data.xml',
        'demo/op_course_material_data.xml',
        'demo/res_users_data.xml',
        'demo/enrollement_demo_data.xml',
        'demo/rating_message_data.xml',
        'demo/op_course_demo2.xml',
        'demo/op_course_demo1.xml',
        'demo/op_course_demo3.xml',
        'demo/op_course_demo4.xml',
        'demo/op_course_demo5.xml',
        'demo/op_course_demo6.xml',
        'demo/op_course_demo_30.xml',
        'demo/op_course_demo_31.xml',
        'demo/op_course_demo_32.xml',
        'demo/op_course_demo_33.xml',
        'demo/op_course_demo_34.xml',
        'demo/op_course_demo_35.xml',
    ],
    'images': [
        'static/description/openeducat_lms_banner.jpg',
    ],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 150,
    'currency': 'EUR',
    'license': 'OPL-1',
    'live_test_url': 'https://www.openeducat.org/plans'
}
