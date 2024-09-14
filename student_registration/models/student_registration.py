from odoo import _ ,models, fields, api
from datetime import date
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


class StudentRegistration(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _name = 'student.registration'
    _description = 'Student Registration'
    _order = 'name'

    # --------------------------------------- Fields Declaration ----------------------------------

    name = fields.Char(string="Registration Number", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    student_id = fields.Many2one('res.partner', string='Student', domain=[('is_student', '=', True)], required=True)
    phone = fields.Char(string='Phone', store=True, readonly=True, compute='_compute_phone')
    age = fields.Integer(compute='_compute_age', string='Age')
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id, readonly=True)
    amount = fields.Monetary(string='Registration Fee', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('invoiced', 'Invoiced'),
        ('canceled', 'Canceled')], default='draft', string='Status', readonly=True)

    invoice_id = fields.Many2one('account.move', string="Invoice", readonly=True)

    # ----------------------------------- Computed Methods --------------------------------

    @api.depends('student_id.phone')
    def _compute_phone(self):
        for record in self:
            if record.state == 'draft':
                record.phone = record.student_id.phone
            else:
                record.phone = record.phone

    # ------------------------------------------ CRUD Methods -------------------------------------

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('student.registration') or _('New')

        # Ensure 'is_student' is checked when creating new students
        student = self.env['res.partner'].browse(vals.get('student_id'))
        if student:
            if not student.is_student:
                raise ValidationError("The selected partner is not marked as a student.")
            if not student.birth_date:
                raise ValidationError("The selected student does not have a birth date.")

        return super(StudentRegistration, self).create(vals)

    # ----------------------------------- Constrains and Onchanges --------------------------------

    @api.depends('student_id.birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.student_id.birth_date:
                rec.age = (date.today() - rec.student_id.birth_date).days // 365
            else:
                rec.age = 0

    # ---------------------------------------- Action Methods -------------------------------------

    def action_confirm(self):
        self.ensure_one()
        self.write({'state': 'confirmed'})

    def action_cancel(self):
        self.ensure_one()
        self.write({'state': 'canceled'})

    def action_confirm_bulk(self):
        """Bulk confirm registrations from the list view."""
        selected_ids = self.env.context.get('active_ids', [])
        if not selected_ids:
            raise UserError("No records selected.")
        registrations = self.env['student.registration'].browse(selected_ids)
        for registration in registrations:
            if registration.state == 'draft':
                registration.action_confirm()
            else:
                raise UserError(f"Registration {registration.name} cannot be confirmed as it is not in draft state.")

    def action_create_invoice(self):
        """Create and link an invoice to this registration."""
        self.ensure_one()
        self.write({'state': 'invoiced'})

        # Prepare invoice values
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.student_id.id,
            'registration_id': self.id,
            'invoice_date': fields.Date.context_today(self),
            'invoice_line_ids': [(0, 0, {
                'name': f"Registration Fees for {self.student_id.name}",
                'quantity': 1,
                'price_unit': self.amount,
                'currency_id': self.currency_id.id,
            })],
        }

        # Create the invoice
        invoice = self.env['account.move'].create(invoice_vals)
        self.invoice_id = invoice.id

        return invoice

    def action_view_invoice(self):
        """Open the related invoice."""
        self.ensure_one()
        if self.invoice_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Invoice',
                'res_model': 'account.move',
                'view_mode': 'form',
                'res_id': self.invoice_id.id,
            }