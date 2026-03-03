from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    sl_api_key = fields.Char(string="Sales Layer API Key", config_parameter='odoo_sales_layer_connector.sl_api_key')
    sl_connector_id = fields.Char(string="Sales Layer Connector ID", config_parameter='odoo_sales_layer_connector.sl_connector_id')
    sl_base_url = fields.Char(string="Sales Layer Base URL", config_parameter='odoo_sales_layer_connector.sl_base_url', default="https://app.saleslayer.com")
    sl_sync_trigger = fields.Selection([
        ('on_write', 'On Write'),
        ('manual', 'Manual Button')
    ], string="Sync Trigger", config_parameter='odoo_sales_layer_connector.sl_sync_trigger', default='manual')
