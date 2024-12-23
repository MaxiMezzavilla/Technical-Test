from odoo import api, fields, models

class SaleChannel(models.Model):
    _name = 'sale.channel'
    _description = 'Sales Channel'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char('Name', required=True, tracking=True)
    code = fields.Char(string='Código', readonly=True, default=lambda self: self._generate_code())
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse')
    journal_id = fields.Many2one('account.journal', 'Journal')

    @api.model
    def _generate_code(self):
        """Genera un código único para cada canal de venta."""
        sequence = self.env['ir.sequence'].next_by_code('sale.channel.code') or 'CH000001'
        return sequence
    
    @api.model
    def create(self, vals):
        """Sobrescribe el método de creación para asignar un código automáticamente."""
        if 'code' not in vals or not vals['code']:
            vals['code'] = self._generate_code()
        return super(SaleChannel, self).create(vals)
