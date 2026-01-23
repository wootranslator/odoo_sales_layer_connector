import base64
import requests
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class SalesLayerController(http.Controller):

    @http.route('/api/saleslayer/sync', type='json', auth='none', methods=['POST'], csrf=False)
    def sync_from_pim(self):
        data = request.jsonrequest
        header_token = request.httprequest.headers.get('Authorization')
        
        config_obj = request.env['ir.config_parameter'].sudo()
        db_token = config_obj.get_param('sl.webhook_token')

        if header_token != f"Bearer {db_token}":
            return {'status': 'error', 'message': 'Unauthorized'}

        source_id = data.get('id_origen')
        variant = request.env['product.product'].sudo().search([('default_code', '=', source_id)], limit=1)

        if not variant:
            return {'status': 'not_found', 'id': source_id}

        vals = {}
        if 'nombre' in data: vals['name'] = data['nombre']
        if 'ean' in data: vals['barcode'] = data['ean']
        
        # Procesar Imagen de Variante
        if data.get('image_url'):
            try:
                res = requests.get(data['image_url'], timeout=10)
                if res.status_code == 200:
                    vals['image_variant_1920'] = base64.b64encode(res.content)
            except Exception as e:
                _logger.error(f"Error imagen: {e}")

        lang = data.get('lang', 'es_ES')
        variant.with_context(lang=lang).sudo().write(vals)
        
        return {'status': 'success', 'odoo_id': variant.id}
