import requests
import json
import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_sl_sync = fields.Boolean(string="Sincronizar con Sales Layer", default=False)
    sl_external_id = fields.Char(string="Sales Layer ID", copy=False)
    sl_status = fields.Selection([
        ('draft', 'Draft'),
        ('synced', 'Synced'),
        ('enriched', 'Fully Enriched'),
        ('error', 'Error')
    ], string="Estado Sales Layer", default='draft', copy=False)
    sl_enrichment_level = fields.Selection([
        ('basic', 'Basic (Purchasing)'),
        ('in_progress', 'In Progress (PIM)'),
        ('completed', 'Completed (Validated)')
    ], string="Nivel de Enriquecimiento", default='basic', copy=False)
    sl_last_error = fields.Text(string="Último Error Sales Layer", readonly=True, copy=False)
    sl_url = fields.Char(string="Sales Layer Link", compute='_compute_sl_url')

    @api.depends('sl_external_id')
    def _compute_sl_url(self):
        # Base URL for the public app might differ from the API URL, but we use the config one.
        # Usually: https://app.saleslayer.com/product/ID
        params = self.env['ir.config_parameter'].sudo()
        api_base = params.get_param('odoo_sales_layer_connector.sl_base_url') or 'https://api2.saleslayer.com/rest/Catalog'
        # Basic guess for the app URL if it's the API one
        app_url = api_base.replace('api2', 'app').replace('/rest/Catalog', '')
        
        for record in self:
            if record.sl_external_id:
                record.sl_url = f"{app_url}/product/{record.sl_external_id}"
            else:
                record.sl_url = False

    def action_sync_to_sales_layer(self):
        """Metodo manual para disparar la sincronizacion"""
        for record in self:
            record.sl_enrichment_level = 'in_progress'
            record._sync_to_sales_layer()

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
        if self.sl_status == 'synced':
            self.write({'sl_status': 'enriched', 'sl_enrichment_level': 'completed'})

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
                'sl_status': 'error',
                'sl_last_error': _("Falta configuración de API Key o Base URL.")
            })
            return

        # API 2.0 Endpoint for Products
        # OData v4.01: POST for creation, PATCH for update
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
            _logger.info("API 2.0 Syncing to Sales Layer: %s", json.dumps(payload, indent=2))
            
            if self.sl_external_id:
                # Update existing record (PATCH)
                update_url = f"{endpoint}('{self.sl_external_id}')"
                # response = requests.patch(update_url, json=payload, headers=headers, timeout=15)
                method = "PATCH"
                final_url = update_url
            else:
                # Create new record (POST)
                # response = requests.post(endpoint, json=payload, headers=headers, timeout=15)
                method = "POST"
                final_url = endpoint
            
            _logger.info(f"Method: {method} to {final_url}")
            
            # Simulamos éxito y asignación de ID
            mock_external_id = self.sl_external_id or f"SL2-{self.id}" 
            
            self.write({
                'sl_external_id': mock_external_id,
                'sl_status': 'synced',
                'sl_last_error': False
            })
            
        except Exception as e:
            _logger.error("Error in Sales Layer API 2.0 Sync: %s", str(e))
            self.write({
                'sl_status': 'error',
                'sl_last_error': str(e)
            })

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
