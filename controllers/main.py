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
        product_data = data.get('product_data', {}) # Datos opcionales para actualizar

        if not sl_id:
            return {'status': 'error', 'message': 'Missing sl_external_id'}

        # Buscar el producto por ID externo de Sales Layer
        product = request.env['product.template'].sudo().search([('sl_external_id', '=', sl_id)], limit=1)
        
        if not product:
            _logger.warning(f"Webhook: Product with sl_external_id {sl_id} not found")
            return {'status': 'not_found'}

        # Lógica de actualización de estado
        if new_status in ['Validated', 'Enriched']:
            vals = {
                'sl_status': 'enriched',
                'sl_enrichment_level': 'completed'
            }
            
            # Consultar toggles de importación
            params = request.env['ir.config_parameter'].sudo()
            
            if params.get_param('odoo_sales_layer_connector.sl_import_sku') and 'sku' in product_data:
                vals['default_code'] = product_data['sku']
            if params.get_param('odoo_sales_layer_connector.sl_import_ean') and 'ean' in product_data:
                vals['barcode'] = product_data['ean']
            if params.get_param('odoo_sales_layer_connector.sl_import_descriptions') and 'description' in product_data:
                vals['description_sale'] = product_data['description']
            if params.get_param('odoo_sales_layer_connector.sl_import_prices') and 'price' in product_data:
                vals['list_price'] = float(product_data['price'])
            if params.get_param('odoo_sales_layer_connector.sl_import_dimensions'):
                if 'weight' in product_data:
                    vals['weight'] = float(product_data['weight'])
                if 'volume' in product_data:
                    vals['volume'] = float(product_data['volume'])
            
            # Imágenes (requiere descargar y convertir a base64)
            if params.get_param('odoo_sales_layer_connector.sl_import_images') and 'image_url' in product_data:
                try:
                    import requests
                    import base64
                    img_res = requests.get(product_data['image_url'], timeout=10)
                    if img_res.status_code == 200:
                        vals['image_1920'] = base64.b64encode(img_res.content)
                except Exception as e:
                    _logger.error(f"Error importing image from webhook: {str(e)}")

            product.write(vals)
            _logger.info(f"Webhook: Product {product.name} updated with Sales Layer data")
            return {'status': 'success', 'message': f'Product {sl_id} updated'}

        return {'status': 'ignored', 'message': 'Status not relevant'}
