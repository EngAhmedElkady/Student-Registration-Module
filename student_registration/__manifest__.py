{
    'name': 'Student Registration Module',
    'version': '1.0',
    'category': 'Education',
    'summary': 'Module for managing student registrations with security-based functionality',
    'description': """
            A custom student registration module for managing student data, registration, and related invoicing in Odoo.
    """,
    'author': 'Ahmed Elkady',
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'base',    # Required for basic Odoo functionalities like res.partner
        'account'  # Required for invoicing functionalities
    ],
    'data': [
        # security
        'security/registration_security.xml',
        'security/ir.model.access.csv',

        # data
        'data/sequence_data.xml',

        # views
        'views/res_partner_views.xml',
        'views/student_registration_views.xml',
        # 'views/calendar_view.xml',

        # menu
        'menu_views.xml',
    ],
}