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
    'depends': ['base', 'account'],
    'data': [
        # security
        'security/registration_security.xml',
        'security/ir.model.access.csv',

        # data
        'data/sequence_data.xml',

        # views
        'views/res_partner_views.xml',
        'views/student_registration_views.xml',

        # menu
        'menu_views.xml',
    ],
}