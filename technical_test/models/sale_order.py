from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_channel_id = fields.Many2one('sale.channel', 'Sales Channel', required=True)
    credit_group_id = fields.Many2one('credit.group', 'Credit Group', required=True)
    credit = fields.Selection(
        [('non_limit', 'Sin limite de credito'), 
         ('available_credit', 'Credito disponible'),
          ('block_credit', 'Credito bloqueado')],
        compute='_compute_credit', 
        string='Credit')

    @api.onchange('sale_channel_id')
    def _onchange_sale_channel_id(self):
        if self.sale_channel_id:
            self.warehouse_id = self.sale_channel_id.warehouse_id

    def _compute_credit(self):
        """Cuando se selecciona un cliente y un canal de venta el
        sistema debe buscar si existe un grupo de crédito dónde está asociado el cliente
        para ese canal. Si no encuentra ningún grupo el valor del campo seguirá siendo Sin
        límite de crédito. Si lo encuentra debe comparar el importe total de la orden de venta
        con el crédito disponible del grupo, si el importe total de la venta supera el crédito
        disponible el valor del campo debe ser Crédito bloqueado, sino lo supera debe ser
        Crédito disponible.
        """
        for record in self:
            record.credit = 'non_limit'
            if record.partner_id and record.sale_channel_id:
                partner_group = record.partner_id.credit_groups.filtered(lambda x: x.sale_channel_id == record.sale_channel_id)
                if partner_group:
                    if record.amount_total > partner_group.credit_available:
                        record.credit = 'block_credit'
                    else:
                        record.credit = 'available_credit'

    def action_confirm(self):
        if self.credit == 'block_credit':
            raise UserError('El crédito disponible no es suficiente para realizar la venta')
        if self.partner_id.credit_groups.credit_available < self.amount_total:
            raise UserError('El crédito disponible no es suficiente para realizar la venta')
        return super(SaleOrder, self).action_confirm()
