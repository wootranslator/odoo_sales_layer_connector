from odoo import models, fields

class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    sl_external_id = fields.Char(string="Sales Layer ID", copy=False)

class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    sl_external_id = fields.Char(string="Sales Layer ID", copy=False)
