from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    sale_channel_id = fields.Many2one('sale.channel', 'Sales Channel', readonly=True)
