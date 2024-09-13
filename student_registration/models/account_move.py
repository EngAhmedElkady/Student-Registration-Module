from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    registration_id = fields.Many2one('student.registration', string='Student Registration', ondelete='set null')
