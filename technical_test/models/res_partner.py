from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    credit_control = fields.Boolean(string='Credit Control')
    credit_groups = fields.Many2many('credit.group', string='Credit Groups')
