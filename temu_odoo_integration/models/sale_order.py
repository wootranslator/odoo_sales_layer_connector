from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    temu_order_id = fields.Char(string='Temu Order ID', copy=False, index=True)
    temu_transaction_id = fields.Char(string='Temu Transaction ID', copy=False)
    is_temu_order = fields.Boolean(string='Is Temu Order', default=False)
