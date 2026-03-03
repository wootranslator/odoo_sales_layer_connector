import requests
import logging
from odoo import models, api, _
_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model_create_multi
    def create(self, vals_list):
        products = super().create(vals_list)
        if not self.env.context.get('skip_sl_sync'):
            trigger = self.env['ir.config_parameter'].sudo().get_param('odoo_sales_layer_connector.sl_sync_trigger')
            if trigger == 'on_write':
                for product in products:
                    if product.product_tmpl_id.is_sl_sync:
                        product.product_tmpl_id.with_context(skip_sl_sync=True)._sync_to_sales_layer()
        return products

    def write(self, vals):
        res = super().write(vals)
        if not self.env.context.get('skip_sl_sync'):
            trigger = self.env['ir.config_parameter'].sudo().get_param('odoo_sales_layer_connector.sl_sync_trigger')
            if trigger == 'on_write':
                for product in self:
                    if product.product_tmpl_id.is_sl_sync:
                        product.product_tmpl_id.with_context(skip_sl_sync=True)._sync_to_sales_layer()
        return res
