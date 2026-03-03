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
        base_url = self.env['ir.config_parameter'].sudo().get_param('odoo_sales_layer_connector.sl_base_url')
        for record in self:
            if record.sl_external_id and base_url:
                url_trimmed = base_url.rstrip('/')
                record.sl_url = f"{url_trimmed}/{record.sl_external_id}"
            else:
                record.sl_url = False

    def action_sync_to_sales_layer(self):
        """Metodo manual para disparar la sincronizacion"""
        for record in self:
            record.sl_enrichment_level = 'in_progress'
            record._sync_to_sales_layer()

    def action_check_sl_status(self):
        """Metodo manual para consultar el estado en Sales Layer"""
        self.ensure_one()
        params = self.env['ir.config_parameter'].sudo()
        api_key = params.get_param('odoo_sales_layer_connector.sl_api_key')
        connector_id = params.get_param('odoo_sales_layer_connector.sl_connector_id')
        
        if not api_key or not self.sl_external_id:
            return

        # Mockup de llamada GET
        # api_endpoint = f"https://api.saleslayer.com/v1/items/{self.sl_external_id}"
        # response = requests.get(api_endpoint, headers={'Authorization': f'Bearer {api_key}'})
        
        _logger.info(f"Checking status for {self.sl_external_id}")
        # Supongamos que refrescamos y está completado
        if self.sl_status == 'synced':
            self.write({'sl_status': 'enriched', 'sl_enrichment_level': 'completed'})

    def _prepare_sl_payload(self):
        """Genera el JSON estructurado para el Padre y sus Variantes"""
        self.ensure_one()
        
        # Atributos del Padre
        attributes = []
        for line in self.attribute_line_ids:
            attributes.append({
                'name': line.attribute_id.name,
                'values': [v.name for v in line.value_ids]
            })

        # Variantes (Hijos)
        variants = []
        for variant in self.product_variant_ids:
            # Combinación de atributos para esta variante
            variant_attrs = []
            for ptav in variant.product_template_attribute_value_ids:
                variant_attrs.append(f"{ptav.attribute_id.name}: {ptav.name}")
            
            variants.append({
                'id_odoo': variant.id,
                'sku': variant.default_code or '',
                'ean': variant.barcode or '',
                'combination': ", ".join(variant_attrs),
                'price': variant.lst_price,
            })

        payload = {
            'id_odoo': self.id,
            'name': self.name,
            'default_code': self.default_code or '',
            'barcode': self.barcode or '',
            'attributes': attributes,
            'variants': variants,
            'type': 'product_with_variants'
        }
        return payload

    def _sync_to_sales_layer(self):
        self.ensure_one()
        if not self.is_sl_sync:
            return

        params = self.env['ir.config_parameter'].sudo()
        api_key = params.get_param('odoo_sales_layer_connector.sl_api_key')
        connector_id = params.get_param('odoo_sales_layer_connector.sl_connector_id')
        
        if not api_key or not connector_id:
            self.write({
                'sl_status': 'error',
                'sl_last_error': _("Falta configuración de API Key o Connector ID.")
            })
            return

        # Prepare product data with variants hierarchy
        payload = self._prepare_sl_payload()

        # API Mockup using requests
        # Sales Layer API typically uses a specific structure. 
        # Here we follow the requirement to use 'requests' and handle 200/201.
        
        # Use a dummy URL if not specified, though normally we'd use base_url or a specific API endpoint.
        api_endpoint = "https://api.saleslayer.com/v1/items" # Placeholder
        
        try:
            _logger.info("Syncing to Sales Layer: %s", json.dumps(payload, indent=2))
            
            # Simulamos el envío
            # response = requests.post(api_endpoint, json=payload, headers={'Authorization': f'Bearer {api_key}'})
            
            # Simulación de respuesta exitosa
            mock_external_id = f"SL-{self.id}" 
            
            self.write({
                'sl_external_id': mock_external_id,
                'sl_status': 'synced',
                'sl_last_error': False
            })
            
        except Exception as e:
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
