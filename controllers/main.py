import base64
import requests
import logging
from odoo import http
from odoo.http import request
_logger = logging.getLogger(__name__)

class SalesLayerWebhook(http.Controller):
    @http.route(['/sales_layer/webhook/update_status', '/saleslayer/sync/callback'], type='json', auth='none', methods=['POST'], csrf=False)
    def update_status(self, token=None):
        """
        Webhook para recibir actualizaciones de estado desde Sales Layer.
        Soporta rutas originales y la especificada en sl_pim_connector.
        """
        params = request.env['ir.config_parameter'].sudo()
        db_token = params.get_param('odoo_sales_layer_connector.sl_webhook_token')
        
        # Validación de token (URL o Header)
        header_token = request.httprequest.headers.get('X-SalesLayer-Token')
        auth_token = token or header_token

        if not auth_token or auth_token != db_token:
            _logger.warning("Webhook Unauthorized: Token mismatch or missing")
            return {'status': 'error', 'message': 'Unauthorized'}

        data = request.jsonrequest
        sl_id = data.get('sl_external_id') or data.get('id')
        new_status = data.get('status')
        product_data = data.get('product_data', {})

        if not sl_id:
            return {'status': 'error', 'message': 'Missing External ID'}

        product = request.env['product.template'].sudo().search([('sl_external_id', '=', sl_id)], limit=1)
        if not product:
            _logger.warning(f"Webhook: Product with sl_external_id {sl_id} not found")
            return {'status': 'not_found'}

        if new_status in ['Validated', 'Enriched', 'synced']:
            vals = {
                'sl_sync_status': 'enriched',
                'sl_last_sync': fields.Datetime.now()
            }
            
            # Field Mapping Logic (Respecting Toggles)
            if params.get_param('odoo_sales_layer_connector.sl_import_sku') and 'sku' in product_data:
                vals['default_code'] = product_data['sku']
            if params.get_param('odoo_sales_layer_connector.sl_import_ean') and 'ean' in product_data:
                vals['barcode'] = product_data['ean']
            if params.get_param('odoo_sales_layer_connector.sl_import_descriptions') and 'description' in product_data:
                vals['description_sale'] = product_data['description']
            if params.get_param('odoo_sales_layer_connector.sl_import_prices') and 'price' in product_data:
                vals['list_price'] = float(product_data['price'])
            
            # Image Import
            if params.get_param('odoo_sales_layer_connector.sl_import_images') and 'image_url' in product_data:
                try:
                    img_res = requests.get(product_data['image_url'], timeout=10)
                    if img_res.status_code == 200:
                        vals['image_1920'] = base64.b64encode(img_res.content)
                except Exception as e:
                    _logger.error(f"Error importing image from webhook: {str(e)}")

            product.write(vals)
            _logger.info(f"Webhook: Product {product.name} synchronized from Sales Layer")
            return {'status': 'success', 'message': f'Product {sl_id} updated'}

        return {'status': 'ignored', 'message': 'Status not relevant'}
