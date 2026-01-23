from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sl_api_url = fields.Char(string="URL API Sales Layer", config_parameter='sl.api_url', default="https://api.saleslayer.com/v1/items")
    sl_api_token = fields.Char(string="Token API Sales Layer", config_parameter='sl.api_token')
    sl_webhook_token = fields.Char(string="Webhook Security Token", config_parameter='sl.webhook_token')
