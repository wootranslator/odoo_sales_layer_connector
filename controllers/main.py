import base64
import requests
import logging
from odoo import http
from odoo.http import request
_logger = logging.getLogger(__name__)

class SalesLayerWebhook(http.Controller):
    @http.route('/sales_layer/webhook/update_status', type='json', auth='none', methods=['POST'], csrf=False)
    def update_status(self, token=None):
        """
        Webhook para recibir actualizaciones de estado desde Sales Layer.
        URL esperada: /sales_layer/webhook/update_status?token=TU_TOKEN
        """
        # Validación de token de seguridad
        db_token = request.env['ir.config_parameter'].sudo().get_param('odoo_sales_layer_connector.sl_webhook_token')
        if not token or token != db_token:
            _logger.warning("Webhook Unauthorized: Token mismatch or missing")
            return {'status': 'error', 'message': 'Unauthorized'}

        data = request.jsonrequest
        sl_id = data.get('sl_external_id')
        new_status = data.get('status') # Ej: 'Validated', 'Enriched'

        if not sl_id:
            return {'status': 'error', 'message': 'Missing sl_external_id'}

        # Buscar el producto por ID externo de Sales Layer
        product = request.env['product.template'].sudo().search([('sl_external_id', '=', sl_id)], limit=1)
        
        if not product:
            _logger.warning(f"Webhook: Product with sl_external_id {sl_id} not found")
            return {'status': 'not_found'}

        # Lógica de actualización de estado
        if new_status in ['Validated', 'Enriched']:
            product.write({
                'sl_status': 'enriched',
                'sl_enrichment_level': 'completed'
            })
            _logger.info(f"Webhook: Product {product.name} updated to Fully Enriched")
            return {'status': 'success', 'message': f'Product {sl_id} updated'}

        return {'status': 'ignored', 'message': 'Status not relevant'}
