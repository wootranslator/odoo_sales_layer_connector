from odoo import models, fields, api

class TemuConnector(models.Model):
    _name = 'temu.connector'
    _description = 'Temu Connector Configuration'

    name = fields.Char(string='Name', required=True)
    client_id = fields.Char(string='Client ID', required=True)
    client_secret = fields.Char(string='Client Secret', required=True, groups="base.group_system")
    access_token = fields.Char(string='Access Token', groups="base.group_system")
    environment = fields.Selection([
        ('production', 'Production'),
        ('sandbox', 'Sandbox'),
    ], string='Environment', default='sandbox', required=True)
    auto_confirm_paid_orders = fields.Boolean(string='Auto-confirm Paid Orders', default=False, help="Automatically confirm sale orders if a valid payment transaction is found.")
    order_prefix = fields.Char(string='Order Prefix', default='TEMU', help="Prefix for sale orders imported from this marketplace.")
    price_source = fields.Selection([
        ('marketplace', 'Use Marketplace Price'),
        ('pricelist', 'Use Odoo Pricelist'),
    ], string='Price Source', default='marketplace', required=True, help="Choose whether to use the price provided by the marketplace or calculate it using an Odoo pricelist.")
    pricelist_id = fields.Many2one('product.pricelist', string='Default Pricelist')
    team_id = fields.Many2one('crm.team', string='Sales Team', default=lambda self: self.env.ref('temu_odoo_integration.sales_team_temu', raise_if_not_found=False))
    default_journal_id = fields.Many2one('account.journal', string='Default Payment Journal')
    api_url = fields.Char(string='API URL', compute='_compute_api_url', store=True, readonly=False)
    
    # Dashboard Fields
    pending_orders_count = fields.Integer(compute='_compute_order_stats')
    shipped_orders_count = fields.Integer(compute='_compute_order_stats')
    total_orders_count = fields.Integer(compute='_compute_order_stats')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], string='Status', default='draft')

    def _compute_order_stats(self):
        for record in self:
            orders = self.env['sale.order'].search([('temu_order_id', '!=', False)])
            # This is a bit simplified, usually you'd filter by a field linking to the connector
            # For now, we assume all temu orders in this instance belong to the active connectors proportionally 
            # or we filter by something specific. Let's refer to sale_order having is_temu_order.
            record.pending_orders_count = self.env['sale.order'].search_count([
                ('is_temu_order', '=', True),
                ('state', '=', 'draft')
            ])
            record.shipped_orders_count = self.env['sale.order'].search_count([
                ('is_temu_order', '=', True),
                ('picking_ids.state', '=', 'done')
            ])
            record.total_orders_count = self.env['sale.order'].search_count([
                ('is_temu_order', '=', True)
            ])

    @api.depends('environment')
    def _compute_api_url(self):
        for record in self:
            if record.environment == 'production':
                record.api_url = 'https://open-api.temu.com'
            else:
                record.api_url = 'https://open-api.temu-sandbox.com'

    def action_confirm(self):
        self.state = 'confirmed'

    def action_draft(self):
        self.state = 'draft'
