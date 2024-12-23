# from odoo import models, fields, api

# class AccountMove(models.Model):
#     _inherit = "account.move"

#     sale_channel_id = fields.Many2one('sale.channel', 'Sales Channel', readonly=True)

#     # @api.model
#     # def create(self, vals):
#     #     """Al momento de crear la orden de venta pisamos el valor del almacén por el del canal de venta
#     #         para que posteriormente se pueda asignar el almacén correcto al picking       
#     #     """
#     #     if sale_channel_id:= vals['sale_channel_id']:
#     #         vals['warehouse_id'] = self.env['sale.channel'].browse(sale_channel_id).warehouse_id.id
#     #     return super().create(vals)
