from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CreditGroup(models.Model):
    _name = 'credit.group'
    _description = 'Credit Group'

    name = fields.Char('Name', required=True)
    code = fields.Char(string='Código', required=True)
    sale_channel_id = fields.Many2one('sale.channel', 'Sales Channel', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.company.currency_id)
    global_credit = fields.Monetary('Global Credit', required=True, currency_field='currency_id')
    credit_used = fields.Monetary('Credit Used', compute='_compute_credit_used', currency_field='currency_id')
    credit_available = fields.Monetary('Credit Available', compute='_compute_credit_available', currency_field='currency_id')

    @api.constrains('code')
    def _check_unique_code(self):
        """Asegura que el código sea único y no sea '026'."""
        for record in self:
            if '026' in record.code:
                raise ValidationError("El código '026' no está permitido.")
            if self.filtered(lambda x: x.code == record.code and x.id != record.id):
                raise ValidationError(f"El código '{record.code}' ya está en uso. Debe ser único.")

    def _compute_credit_used(self):
        """El valor se obtiene a partir de la sumatoria del total de ventas confirmadas sin facturar, 
        más el total de facturas impagas asociadas a los clientes del grupo de crédito.
        """
        SaleOrder = self.env['sale.order'].search([])
        AccountMove = self.env['account.move'].search([])
        for record in self:
            orders = SaleOrder.filtered(lambda x:  record.id in x.partner_id.credit_groups.ids  and x.state == 'sale' and \
                                        x.invoice_status == 'to invoice')
            invoices = AccountMove.filtered(lambda x: record.id in x.partner_id.credit_groups.ids and x.state == 'posted' \
                                            and x.payment_state == 'not_paid')

            record.credit_used = sum(orders.mapped('amount_total')) + sum(invoices.mapped('amount_total'))

    def _compute_credit_available(self):
        """El valor se obtiene a partir de la resta del crédito global menos el crédito usado."""
        for record in self:
            record.credit_available = record.global_credit - record.credit_used
