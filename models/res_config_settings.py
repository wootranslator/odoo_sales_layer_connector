from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    sl_api_key = fields.Char(string="Sales Layer API Key", config_parameter='odoo_sales_layer_connector.sl_api_key')
    sl_connector_id = fields.Char(string="Sales Layer Connector ID", config_parameter='odoo_sales_layer_connector.sl_connector_id')
    sl_base_url = fields.Char(string="Sales Layer Base URL", config_parameter='odoo_sales_layer_connector.sl_base_url', default="https://api2.saleslayer.com/rest/Catalog")
    sl_sync_trigger = fields.Selection([
        ('on_write', 'On Write'),
        ('manual', 'Manual Button')
    ], string="Sync Trigger", config_parameter='odoo_sales_layer_connector.sl_sync_trigger', default='manual')

    # Field Sync Toggles
    sl_sync_sku = fields.Boolean(string="Sync SKU/Internal Reference", config_parameter='odoo_sales_layer_connector.sl_sync_sku', default=True)
    sl_sync_ean = fields.Boolean(string="Sync EAN/Barcode", config_parameter='odoo_sales_layer_connector.sl_sync_ean', default=True)
    sl_sync_images = fields.Boolean(string="Sync Images", config_parameter='odoo_sales_layer_connector.sl_sync_images', default=True)
    sl_sync_categories = fields.Boolean(string="Sync Categories", config_parameter='odoo_sales_layer_connector.sl_sync_categories', default=True)
    sl_sync_dimensions = fields.Boolean(string="Sync Weight & Volume", config_parameter='odoo_sales_layer_connector.sl_sync_dimensions', default=True)
    sl_sync_descriptions = fields.Boolean(string="Sync Descriptions", config_parameter='odoo_sales_layer_connector.sl_sync_descriptions', default=True)
    sl_sync_prices = fields.Boolean(string="Sync Prices", config_parameter='odoo_sales_layer_connector.sl_sync_prices', default=True)
    sl_sync_attributes = fields.Boolean(string="Sync Attributes", config_parameter='odoo_sales_layer_connector.sl_sync_attributes', default=True)
