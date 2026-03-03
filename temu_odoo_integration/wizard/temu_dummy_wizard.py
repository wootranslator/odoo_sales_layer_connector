from odoo import models, fields, api, _

class TemuDummyWizard(models.TransientModel):
    _name = 'temu.dummy.wizard'
    _description = 'Temu Dummy Data Wizard'

    def action_install_dummy_data(self):
        # 1. Create a dummy marketplace if none exists
        Connector = self.env['temu.connector']
        connector = Connector.search([], limit=1)
        if not connector:
            connector = Connector.create({
                'name': 'Temu Dummy Marketplace',
                'client_id': 'dummy_id',
                'client_secret': 'dummy_secret',
                'environment': 'sandbox',
            })
            connector.action_confirm()

        # 2. Find or create a partner
        Partner = self.env['res.partner']
        partner = Partner.search([('vat', '=', 'B12345678')], limit=1)
        if not partner:
            partner = Partner.create({
                'name': 'Juan Perez (Demo)',
                'email': 'juan.perez@example.com',
                'vat': 'B12345678',
                'country_id': self.env.ref('base.es').id,
            })

        # 3. Create a dummy order
        SaleOrder = self.env['sale.order']
        # Try to find a dummy product or use the first one
        product = self.env['product.product'].search([], limit=1)
        
        order_vals = {
            'partner_id': partner.id,
            'temu_order_id': 'DUMMY-001',
            'is_temu_order': True,
            'team_id': self.env.ref('temu_odoo_integration.sales_team_temu', raise_if_not_found=False).id,
            'order_line': [(0, 0, {
                'product_id': product.id,
                'product_uom_qty': 1,
                'price_unit': 42.50,
            })]
        }
        
        if connector.order_prefix:
            order_vals['name'] = f"{connector.order_prefix}/DUMMY-001"
            
        SaleOrder.create(order_vals)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Dummy Data Installed'),
                'message': _('A sample marketplace and order have been created.'),
                'sticky': False,
            }
        }
