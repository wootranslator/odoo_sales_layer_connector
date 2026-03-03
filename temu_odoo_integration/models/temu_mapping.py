from odoo import models, fields

class TemuMappingProduct(models.Model):
    _name = 'temu.mapping.product'
    _description = 'Temu Product Mapping'

    connector_id = fields.Many2one('temu.connector', string='Connector', required=True)
    temu_sku = fields.Char(string='Temu SKU', required=True)
    product_id = fields.Many2one('product.product', string='Odoo Product', required=True)

class TemuMappingFiscal(models.Model):
    _name = 'temu.mapping.fiscal'
    _description = 'Temu Fiscal Position Mapping'

    connector_id = fields.Many2one('temu.connector', string='Connector', required=True)
    temu_region = fields.Char(string='Temu Region/Country')
    fiscal_position_id = fields.Many2one('account.fiscal.position', string='Fiscal Position', required=True)

class TemuMappingPayment(models.Model):
    _name = 'temu.mapping.payment'
    _description = 'Temu Payment Mapping'

    connector_id = fields.Many2one('temu.connector', string='Connector', required=True)
    temu_payment_method = fields.Char(string='Temu Payment Method', required=True)
    journal_id = fields.Many2one('account.journal', string='Payment Journal', required=True)

class TemuMappingShipping(models.Model):
    _name = 'temu.mapping.shipping'
    _description = 'Temu Shipping Mapping'

    connector_id = fields.Many2one('temu.connector', string='Connector', required=True)
    temu_shipping_method = fields.Char(string='Temu Shipping Method', required=True)
    carrier_id = fields.Many2one('delivery.carrier', string='Odoo Carrier', required=True)

class TemuMappingTax(models.Model):
    _name = 'temu.mapping.tax'
    _description = 'Temu Tax Mapping'

    connector_id = fields.Many2one('temu.connector', string='Connector', required=True)
    temu_tax_name = fields.Char(string='Temu Tax Name/Rate', required=True)
    tax_id = fields.Many2one('account.tax', string='Odoo Tax', required=True)

class TemuMappingTax(models.Model):
    _name = 'temu.mapping.tax'
    _description = 'Temu Tax Mapping'

    connector_id = fields.Many2one('temu.connector', string='Connector', required=True)
    temu_tax_name = fields.Char(string='Temu Tax Name/Rate', required=True)
    tax_id = fields.Many2one('account.tax', string='Odoo Tax', required=True)
