from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class TemuOrderImport(models.TransientModel):
    _name = 'temu.order.import'
    _description = 'Import Orders from Temu'

    connector_id = fields.Many2one('temu.connector', string='Connector', required=True)
    date_from = fields.Datetime(string='Date From')
    date_to = fields.Datetime(string='Date To')

    def _find_or_create_partner(self, order_data):
        """Deduplicate partners by VAT (CIF), email, or name."""
        Partner = self.env['res.partner']
        vat = order_data.get('vat')
        email = order_data.get('email')
        name = order_data.get('partner_name')
        
        partner = False
        if vat:
            # Clean VAT string to ensure consistency
            vat = vat.strip().replace(" ", "").upper()
            partner = Partner.search([('vat', '=', vat)], limit=1)
            
        if not partner and email:
            partner = Partner.search([('email', '=', email)], limit=1)
        
        if not partner and name:
            partner = Partner.search([('name', '=', name)], limit=1)
            
        if not partner:
            partner = Partner.create({
                'name': name,
                'email': email,
                'vat': vat,
                'is_company': False,
                'country_id': self.env.ref('base.es').id if order_data.get('region') == 'ES' else False,
            })
        return partner

    def action_import_orders(self):
        """Main logic to fetch and create orders."""
        self.ensure_one()
        # This is a skeleton logic. In a real scenario, this would call the Temu API service.
        _logger.info("Starting Temu order import for connector %s", self.connector_id.name)
        
        # Simulated API Response
        mock_orders = [
            {
                'order_id': 'TEMU-12345',
                'partner_name': 'Juan Perez',
                'sku': 'PROD-001',
                'qty': 2,
                'price': 15.50,
                'payment_method': 'Credit Card',
                'shipping_method': 'Standard',
                'region': 'ES',
                'transaction_id': 'TXN-998877',
                'payment_status': 'paid',
                'email': 'juan.perez@example.com',
                'vat': 'B12345678',
                'tax_name': 'VAT 21%',
            }
        ]
        
        for order_data in mock_orders:
            # 1. Check if order exists
            existing = self.env['sale.order'].search([('temu_order_id', '=', order_data['order_id'])])
            if existing:
                continue
            
            # 2. Map SKU
            mapping = self.env['temu.mapping.product'].search([
                ('connector_id', '=', self.connector_id.id),
                ('temu_sku', '=', order_data['sku'])
            ], limit=1)
            
            product = mapping.product_id if mapping else self.env['product.product'].search([('default_code', '=', order_data['sku'])], limit=1)
            
            if not product:
                _logger.warning("Product not found for SKU %s", order_data['sku'])
                continue
            
            # 3. Handle Partner (Deduplicated)
            partner = self._find_or_create_partner(order_data)
            
            # 4. Create Sale Order
            sale_order_vals = {
                'partner_id': partner.id,
                'temu_order_id': order_data['order_id'],
                'temu_transaction_id': order_data.get('transaction_id'),
                'is_temu_order': True,
                'team_id': self.connector_id.team_id.id if self.connector_id.team_id else self.env.ref('temu_odoo_integration.sales_team_temu', raise_if_not_found=False).id,
                'pricelist_id': self.connector_id.pricelist_id.id if self.connector_id.price_source == 'pricelist' else partner.property_product_pricelist.id,
                'order_line': [(0, 0, {
                    'product_id': product.id,
                    'product_uom_qty': order_data['qty'],
                    'price_unit': order_data['price'] if self.connector_id.price_source == 'marketplace' else 0.0,
                })]
            }
            
            # Application of Order Prefix
            if self.connector_id.order_prefix:
                # We can either override the name or let Odoo sequence it and just store the prefix
                # Here we will prepend the prefix to the Temu ID for the Odoo name
                sale_order_vals['name'] = f"{self.connector_id.order_prefix}/{order_data['order_id']}"
            
            sale_order = self.env['sale.order'].create(sale_order_vals)
            
            # 4b. Apply Taxes if mapped
            tax_mapping = self.env['temu.mapping.tax'].search([
                ('connector_id', '=', self.connector_id.id),
                ('temu_tax_name', '=', order_data.get('tax_name'))
            ], limit=1)
            if tax_mapping:
                sale_order.order_line.write({'tax_id': [(6, 0, [tax_mapping.tax_id.id])]})
            
            # 5. Handle Fiscal Mapping (Simplified)
            fiscal_mapping = self.env['temu.mapping.fiscal'].search([
                ('connector_id', '=', self.connector_id.id),
                ('temu_region', '=', order_data['region'])
            ], limit=1)
            if fiscal_mapping:
                sale_order.fiscal_position_id = fiscal_mapping.fiscal_position_id
            
            # 6. Handle Shipping Mapping
            shipping_mapping = self.env['temu.mapping.shipping'].search([
                ('connector_id', '=', self.connector_id.id),
                ('temu_shipping_method', '=', order_data['shipping_method'])
            ], limit=1)
            if shipping_mapping:
                sale_order.carrier_id = shipping_mapping.carrier_id.id
            
            # 7. Workflow: Auto-confirm if paid
            if self.connector_id.auto_confirm_paid_orders and order_data.get('payment_status') == 'paid':
                _logger.info("Auto-confirming paid order %s", sale_order.name)
                sale_order.action_confirm()
                
                # Logic to create payment/invoice could go here
                # (Creating a dummy journal entry or payment register if mapping exists)
                self._handle_payment_creation(sale_order, order_data)

    def _handle_payment_creation(self, sale_order, order_data):
        """Register payment if mapping exists."""
        payment_mapping = self.env['temu.mapping.payment'].search([
            ('connector_id', '=', self.connector_id.id),
            ('temu_payment_method', '=', order_data.get('payment_method'))
        ], limit=1)
        
        if payment_mapping:
            # Create a payment record in Odoo
            _logger.info("Registering payment for order %s using journal %s", sale_order.name, payment_mapping.journal_id.name)
            
            # In Odoo 18, we use account.payment or bank statements. 
            # Here we create a simple payment tied to the order's invoice or just as a standalone payment.
            payment = self.env['account.payment'].create({
                'amount': sale_order.amount_total,
                'payment_type': 'inbound',
                'partner_type': 'customer',
                'partner_id': sale_order.partner_id.id,
                'journal_id': payment_mapping.journal_id.id,
                'ref': f"Temu Payment for {sale_order.temu_order_id} (TX: {order_data.get('transaction_id')})",
            })
            payment.action_post()
            # If the order is invoiced, we would reconcile here.
            
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Import Complete'),
                'message': _('Orders have been processed.'),
                'sticky': False,
            }
        }
