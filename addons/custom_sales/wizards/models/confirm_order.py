from datetime import date, datetime
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class ConfirmOrderWizard(models.TransientModel):
    _name = "sale_order.confirm_wizard"
    _description = "Wizard para confirmacion y vista previa del auto ordenamiento de lineas de pedido"

    message = fields.Char(string="Mensaje", required=True)
    sales_order = fields.Many2one("sale.order", string="Pedido", required=True)
    order_line_ids = fields.Many2many("sale.order.line", string="Lineas de pedido", required=True)

    #ACTIONS
    def action_confirm(self):
        self.ensure_one()
        #order lines at sale_order by products and sum quantities
        self.sales_order.group_duplicate_lines()
        #then confirm the order
        self.sales_order.action_confirm()
        
        return {"type": "ir.actions.act_window_close"}
      
    def action_cancel(self):
        self.ensure_one()

        return {"type": "ir.actions.act_window_close"}
        
