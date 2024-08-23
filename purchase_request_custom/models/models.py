from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime

class PurchaseRequestLineMakePurchaseOrderCustom(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.order"
    _description = "Extended Purchase Request Line Make Purchase Order"

    def make_purchase_order(self):
        res = []
        purchase_obj = self.env["purchase.order"]
        po_line_obj = self.env["purchase.order.line"]
        pr_line_obj = self.env["purchase.request.line"]
        purchase = False

        for item in self.item_ids:
            line = item.line_id
            if item.product_qty <= 0.0:
                raise UserError(_("Enter a positive quantity."))
            if self.purchase_order_id:
                purchase = self.purchase_order_id
            if not purchase:
                po_data = self._prepare_purchase_order(
                    line.request_id.picking_type_id,
                    line.request_id.group_id,
                    line.company_id,
                    line.origin,
                )
                purchase = purchase_obj.create(po_data)

            # Crear una nueva línea de orden de compra sin buscar líneas existentes
            po_line_data = self._prepare_purchase_order_line(purchase, item)
            po_line_data["name"] = line.name  # Conservar la descripción
            po_line = po_line_obj.create(po_line_data)

            # Asignar cantidades
            alloc_uom = line.product_uom_id or item.product_uom_id
            po_line_product_uom_qty = po_line.product_uom._compute_quantity(
                po_line.product_uom_qty, alloc_uom
            )
            wizard_product_uom_qty = item.product_uom_id._compute_quantity(
                item.product_qty, alloc_uom
            )
            all_qty = min(po_line_product_uom_qty, wizard_product_uom_qty)
            self.create_allocation(po_line, line, all_qty, alloc_uom)

            # Calcular la nueva cantidad y actualizar la fecha planificada
            new_qty = pr_line_obj._calc_new_qty(line, po_line=po_line, new_pr_line=True)
            po_line.product_qty = new_qty
            date_required = item.line_id.date_required
            po_line.date_planned = datetime(
                date_required.year, date_required.month, date_required.day
            )
            res.append(purchase.id)

        return {
            "domain": [("id", "in", res)],
            "name": _("RFQ"),
            "view_mode": "tree,form",
            "res_model": "purchase.order",
            "view_id": False,
            "context": False,
            "type": "ir.actions.act_window",
        }