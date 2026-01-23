import requests
import logging
from odoo import models, api, _

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model_create_multi
    def create(self, vals_list):
        products = super(ProductProduct, self).create(vals_list)
        for product in products:
            if product.default_code:
                self._send_to_sales_layer(product)
        return products

    def _send_to_sales_layer(self, product):
        get_param = self.env['ir.config_parameter'].sudo().get_param
        url = get_param('sl.api_url')
        token = get_param('sl.api_token')

        if not url or not token:
            return

        payload = {
            "source_id": product.default_code,
            "name": product.name,
            "type": "variant",
            "parent_id": product.product_tmpl_id.id
        }
        
        try:
            # requests.post(url, json=payload, headers={'Authorization': f'Bearer {token}'}, timeout=5)
            _logger.info(f"Sincronización inicial enviada para {product.default_code}")
        except Exception as e:
            _logger.error(f"Fallo en Sales Layer: {str(e)}")
