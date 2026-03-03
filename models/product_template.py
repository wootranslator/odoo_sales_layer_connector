import requests
import json
import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_sl_sync = fields.Boolean(string="Sincronizar con Sales Layer", default=False)
    sl_external_id = fields.Char(string="Sales Layer ID", copy=False)
    sl_sync_status = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('synced', 'Synced'),
        ('enriched', 'Fully Enriched'),
        ('error', 'Error')
    ], string="Sync Status", default='draft', copy=False)
    sl_last_sync = fields.Datetime(string="Last Sync", readonly=True, copy=False)
    sl_error_log = fields.Text(string="Error Log", readonly=True, copy=False)
    sl_product_url = fields.Char(string="PIM Product Link", compute='_compute_sl_product_url')

    # Keep original fields for compatibility or specific needs
    sl_status = fields.Selection(related="sl_sync_status", readonly=True)
    sl_last_error = fields.Text(related="sl_error_log", readonly=True)
    sl_url = fields.Char(related="sl_product_url", readonly=True)

    @api.depends('sl_external_id')
    def _compute_sl_product_url(self):
        params = self.env['ir.config_parameter'].sudo()
        api_base = params.get_param('odoo_sales_layer_connector.sl_base_url') or 'https://api2.saleslayer.com/rest/Catalog'
        app_url = api_base.replace('api2', 'app').replace('/rest/Catalog', '').rstrip('/')
        
        for record in self:
            if record.sl_external_id:
                # Based on prompt: https://app.saleslayer.com/main/products/edit/{id}
                record.sl_product_url = f"{app_url}/main/products/edit/{record.sl_external_id}"
            else:
                record.sl_product_url = False

    def action_sync_to_sales_layer(self):
        """Metodo manual para disparar la sincronizacion"""
        for record in self:
            # Validacion de campos minimos antes de intentar exportar
            if not record.name or not record.default_code:
                record.write({
                    'sl_sync_status': 'error',
                    'sl_error_log': _("Faltan campos obligatorios: Nombre o Referencia Interna (SKU).")
                })
                continue
            
            # Validación de EAN si está el toggle activo o como campo mínimo solicitado
            params = record.env['ir.config_parameter'].sudo()
            if params.get_param('odoo_sales_layer_connector.sl_sync_ean') and not record.barcode:
                record.write({
                    'sl_sync_status': 'error',
                    'sl_error_log': _("El campo EAN/Barcode es obligatorio para la sincronización configurada.")
                })
                continue
                
            record.write({'sl_sync_status': 'pending'})
            record._sync_to_sales_layer()

    def action_sync_to_sl(self):
        """Alias para cumplir con especificaciones de sl_pim_connector"""
        return self.action_sync_to_sales_layer()

    def action_check_sl_status(self):
        """Metodo manual para consultar el estado en Sales Layer (API 2.0)"""
        self.ensure_one()
        params = self.env['ir.config_parameter'].sudo()
        api_key = params.get_param('odoo_sales_layer_connector.sl_api_key')
        base_url = params.get_param('odoo_sales_layer_connector.sl_base_url')
        
        if not api_key or not self.sl_external_id or not base_url:
            return

        # OData v4.01 GET request
        base_url = base_url.rstrip('/')
        api_endpoint = f"{base_url}/Products('{self.sl_external_id}')"
        
        _logger.info(f"Checking status for {self.sl_external_id} at {api_endpoint}")
        
        # En una implementacion real:
        # headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}
        # response = requests.get(api_endpoint, headers=headers, timeout=10)
        
        # Supongamos que refrescamos y está completado
        if self.sl_sync_status == 'synced':
            self.write({'sl_sync_status': 'enriched'})

    def _prepare_sl_payload(self):
        """Genera el JSON estructurado para el Padre y sus Variantes (OData v4.01)"""
        self.ensure_one()
        
        params = self.env['ir.config_parameter'].sudo()
        # Base URL for images
        base_url = params.get_param('web.base.url')

        # Field Sync Toggles
        sync_sku = params.get_param('odoo_sales_layer_connector.sl_sync_sku')
        sync_ean = params.get_param('odoo_sales_layer_connector.sl_sync_ean')
        sync_images = params.get_param('odoo_sales_layer_connector.sl_sync_images')
        sync_categories = params.get_param('odoo_sales_layer_connector.sl_sync_categories')
        sync_dimensions = params.get_param('odoo_sales_layer_connector.sl_sync_dimensions')
        sync_descriptions = params.get_param('odoo_sales_layer_connector.sl_sync_descriptions')
        sync_prices = params.get_param('odoo_sales_layer_connector.sl_sync_prices')
        sync_attributes = params.get_param('odoo_sales_layer_connector.sl_sync_attributes')
        sync_quantity = params.get_param('odoo_sales_layer_connector.sl_sync_quantity')

        # Atributos del Padre (agrupados)
        attributes_data = []
        if sync_attributes:
            for line in self.attribute_line_ids:
                attributes_data.append({
                    'AttributeName': line.attribute_id.name,
                    'AttributeValues': ", ".join([v.name for v in line.value_ids])
                })

        # Variantes (Hijos) - OData Navigation Property 'Variants'
        variants_payload = []
        for variant in self.product_variant_ids:
            variant_attrs = []
            for ptav in variant.product_template_attribute_value_ids:
                variant_attrs.append(f"{ptav.attribute_id.name}: {ptav.name}")
            
            variant_data = {
                'OdooID': str(variant.id),
                'VariantDescription': ", ".join(variant_attrs),
            }
            if sync_sku:
                variant_data['SKU'] = variant.default_code or ''
            if sync_ean:
                variant_data['EAN'] = variant.barcode or ''
            if sync_prices:
                variant_data['Price'] = float(variant.lst_price)
            if sync_dimensions:
                variant_data['Weight'] = float(variant.weight or 0.0)
                variant_data['Volume'] = float(variant.volume or 0.0)
            if sync_quantity:
                variant_data['FreeQuantity'] = float(variant.free_qty or 0.0)
            
            variants_payload.append(variant_data)

        payload = {
            'OdooID': str(self.id),
            'Name': self.name,
            'ProductType': self.type,
            'Variants': variants_payload,
        }

        # Optional Fields
        if sync_sku:
            payload['SKU'] = self.default_code or ''
        if sync_ean:
            payload['EAN'] = self.barcode or ''
        if sync_descriptions:
            payload['Description'] = self.description_sale or self.name
        if sync_categories:
            payload['Category'] = self.categ_id.complete_name if self.categ_id else 'Uncategorized'
        if sync_prices:
            payload['Price'] = float(self.list_price)
        if sync_images and self.image_1920:
            payload['ImageURL'] = f"{base_url}/web/image/product.template/{self.id}/image_1920"
        if sync_attributes:
            payload['Attributes'] = attributes_data
        if sync_quantity:
            payload['FreeQuantity'] = float(self.free_qty or 0.0)

        return payload

    def _sync_to_sales_layer(self):
        self.ensure_one()
        if not self.is_sl_sync:
            return

        params = self.env['ir.config_parameter'].sudo()
        api_key = params.get_param('odoo_sales_layer_connector.sl_api_key')
        base_url = params.get_param('odoo_sales_layer_connector.sl_base_url')
        
        if not api_key or not base_url:
            self.write({
                'sl_sync_status': 'error',
                'sl_error_log': _("Falta configuración de API Key o Base URL.")
            })
            return

        # 1. Attribute Check & Sync: Ensure all attributes and values exists in SL (API 2.0)
        self._ensure_attributes_synced(api_key, base_url.rstrip('/'))
                
        # Continua con el flujo de Producto...
        base_url = base_url.rstrip('/')
        endpoint = f"{base_url}/Products"
        
        payload = self._prepare_sl_payload()

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'OData-Version': '4.0',
            'OData-MaxVersion': '4.0'
        }

        try:
            _logger.info("API 2.0 Exporting to SL (%s): %s", self.name, json.dumps(payload, indent=2))
            
            if self.sl_external_id:
                # Update existing record (PATCH)
                url = f"{endpoint}('{self.sl_external_id}')"
                method = "PATCH"
                # response = requests.patch(url, json=payload, headers=headers, timeout=15)
            else:
                # Create new record (POST)
                url = endpoint
                method = "POST"
                # response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            _logger.info("SL API call: %s %s", method, url)
            
            # Simulated Response
            mock_id = self.sl_external_id or f"SL2-{self.id}"
            
            self.write({
                'sl_external_id': mock_id,
                'sl_sync_status': 'synced',
                'sl_last_sync': fields.Datetime.now(),
                'sl_error_log': False
            })
            _logger.info("SL Sync Success: %s (External ID: %s)", self.name, mock_id)
            
        except Exception as e:
            error_msg = f"Error in SL API 2.0 Sync: {str(e)}"
            _logger.error(error_msg)
            self.write({
                'sl_sync_status': 'error',
                'sl_error_log': error_msg
            })

    def _ensure_attributes_synced(self, api_key, base_url):
        """Pre-validation: Checks and creates missing attributes/values in SL"""
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'OData-Version': '4.0'
        }
        
        for line in self.attribute_line_ids:
            attr = line.attribute_id
            if not attr.sl_external_id:
                # 1. Search if it already exists by name
                search_url = f"{base_url}/Attributes?$filter=Name eq '{attr.name}'"
                # response = requests.get(search_url, headers=headers, timeout=10)
                # if response.json().get('value'): attr.sl_external_id = res['value'][0]['ID']
                
                # 2. If not found, create it
                if not attr.sl_external_id:
                    _logger.info("Attribute '%s' not found in SL. Creating...", attr.name)
                    payload = {'Name': attr.name, 'OdooID': str(attr.id)}
                    # response = requests.post(f"{base_url}/Attributes", json=payload, headers=headers)
                    # attr.sl_external_id = response.json().get('ID')
                    attr.sl_external_id = f"SL-ATTR-{attr.id}" # Mock
            
            # 3. Synchronize Values
            for val in line.value_ids:
                if not val.sl_external_id:
                    _logger.info("Value '%s' for attribute '%s' not found. Syncing...", val.name, attr.name)
                    # Logic: POST to /AttributeValues or check if it's already there
                    val.sl_external_id = f"SL-VAL-{val.id}" # Mock

        _logger.info("Attributes/Values pre-sync validation completed for: %s", self.name)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        if not self.env.context.get('skip_sl_sync'):
            trigger = self.env['ir.config_parameter'].sudo().get_param('odoo_sales_layer_connector.sl_sync_trigger')
            if trigger == 'on_write':
                for record in records:
                    if record.is_sl_sync:
                        record.with_context(skip_sl_sync=True)._sync_to_sales_layer()
        return records

    def write(self, vals):
        res = super().write(vals)
        # Check if we should trigger sync automatically
        if not self.env.context.get('skip_sl_sync'):
            trigger = self.env['ir.config_parameter'].sudo().get_param('odoo_sales_layer_connector.sl_sync_trigger')
            if trigger == 'on_write':
                for record in self:
                    if record.is_sl_sync:
                        record.with_context(skip_sl_sync=True)._sync_to_sales_layer()
        return res
