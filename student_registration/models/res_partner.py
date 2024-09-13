from email.policy import default

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class ResPartner(models.Model):

    _inherit = 'res.partner'

    is_student = fields.Boolean(string="Is Student")
    birth_date = fields.Date(string="Birth Date")

    # ----------------------------------- Constrains and Onchanges --------------------------------

    @api.constrains('birth_date')
    def _check_birth_date(self):
        for rec in self:
            if rec.birth_date and rec.birth_date > date.today():
                raise ValidationError("The birth date cannot be in the future.")

    # @api.onchange('is_student')
    # def _onchange_is_student(self):
    #     if self.is_student and not self.birth_date:
    #         raise ValidationError("Birth Date is required for students.")
