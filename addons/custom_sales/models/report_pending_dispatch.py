from odoo import models, fields, tools

class ReportPendingDispatch(models.Model):
    _name = "report.pending.dispatch"
    _description = "Reporte de productos pendientes por despachar"
    _auto = False
    _order = "invoice_date desc"

    product_id = fields.Many2one("product.product", string="Producto")
    partner_id = fields.Many2one("res.partner", string="Cliente")
    sale_order_id = fields.Many2one("sale.order", string="Orden de Venta")
    invoice_id = fields.Many2one("account.move", string="Factura")
    invoice_date = fields.Date(string="Fecha de Factura")
    quantity = fields.Float(string="Cantidad Facturada")

    #am = account move 
    #sol = sale order line
    #so = sale order
    #sp = stock picking
    
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW report_pending_dispatch AS (
                SELECT
                    MIN(sol.id) AS id,
                    sol.product_id,
                    so.partner_id,
                    so.id AS sale_order_id,
                    am.id AS invoice_id,
                    am.invoice_date,
                    sol.product_uom_qty AS quantity
                FROM sale_order_line sol
                JOIN sale_order so ON sol.order_id = so.id
                JOIN account_move am ON am.invoice_origin = so.name
                JOIN stock_picking sp ON sp.origin = so.name
                WHERE so.state = 'sale'
                  AND am.move_type = 'out_invoice'
                  AND am.state = 'posted'
                  AND sp.state IN ('waiting', 'confirmed', 'assigned')
                GROUP BY sol.product_id, so.partner_id, so.id, am.id, am.invoice_date, sol.product_uom_qty
            )
        """)