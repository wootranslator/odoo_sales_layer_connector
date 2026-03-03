from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    temu_shipment_id = fields.Char(string='Temu Shipment ID', copy=False)
    temu_tracking_number = fields.Char(string='Temu Tracking Number', copy=False)
    temu_status = fields.Char(string='Temu Fulfillment Status', readonly=True)

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        for picking in self:
            if picking.sale_id and picking.sale_id.is_temu_order:
                picking._sync_tracking_to_temu()
        return res

    def _sync_tracking_to_temu(self):
        """Logic to send tracking number back to Temu."""
        for picking in self:
            if not picking.carrier_tracking_ref:
                continue
            # Here we would call the Temu API to update shipment status
            self.temu_tracking_number = picking.carrier_tracking_ref
            self.temu_status = 'shipped'
            # API call simulation:
            # client = picking.sale_id.connector_id._get_api_client()
            # client.update_tracking(picking.temu_shipment_id, picking.carrier_tracking_ref)
