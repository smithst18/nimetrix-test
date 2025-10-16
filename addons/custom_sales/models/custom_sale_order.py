from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError
import logging
_logger = logging.getLogger(__name__)


class CustomSaleOrder(models.Model):
    _inherit = "sale.order"
    _description = "Modelo Custom heredado de Sale.order"
    
    #FIELDS
    #ONCHANGES
    #COMPUTES
    
    #METHODS
    #this function is used to group duplicated products
    def group_duplicate_lines(self):
        """group lines with the same product, sum the quantities."""
        grouped = {}
        to_unlink = []

        for line in self.order_line:
            # Create a unique immutable key
            #tax cant be mutable because it is a many2many fields must be tuple to be hashable
            key = (line.product_id.id, line.price_unit, line.product_uom, line.discount, tuple(line.tax_id.ids))

            #if key not in group, add the line to the group
            if key not in grouped:
                grouped[key] = line
                
            else:
                #update line with its ref db and sum the quantity of the line to the existing line
                grouped[key].product_uom_qty += line.product_uom_qty

                # remove the duplicated line
                to_unlink.append(line.id)
                
        if len(to_unlink) > 0:
            self.env['sale.order.line'].browse(to_unlink).unlink()
                
    #this function is used to check if there are duplicated products
    def _check_duplicate_lines(self):
        """Return True if any product appears more than once."""
        product_ids = [line.product_id.id for line in self.order_line]
        #if the leng changed, there are duplicated products
        if len(product_ids) != len(set(product_ids)):
            return True
          
        return False
        
    #this function is used to confirm the order with the wizard view
    def action_confirm_order(self):
        self.ensure_one()
        
        if self._check_duplicate_lines():
          
            return {
                "name": "Confirmación",
                "type": "ir.actions.act_window",
                "res_model": "sale_order.confirm_wizard",
                "view_mode": "form",
                "target": "new",
                "context": {
                    "default_message": "El pedido tiene productos duplicados se van a unificar en una sola linea",
                    "default_sales_order": self.id,
                    "default_order_line_ids": self.order_line.ids,
                },
            }
        else:
            #if there are no duplicated products, call the action_confirm method of the sale.order model
            self.action_confirm()

        
    def action_confirm(self):
      
        res = super().action_confirm()
        
        return res
                