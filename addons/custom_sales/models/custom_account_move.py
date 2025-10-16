from odoo import fields, models, api
from odoo.tools import float_compare, float_is_zero

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _compute_amount(self):
        """recalcular las líneas de impuesto en Bs.F y luego llamar al super"""
        # recorrer sólo las facturas (invoices/receipts) que están en moneda extranjera
        for move in self.filtered(lambda m: 
            m.is_invoice(include_receipts=True) and 
            m.currency_id != m.company_id.currency_id and
            m.invoice_currency_rate
        ):
            # Recalcular las líneas de impuesto basadas en la base imponible en Bs.F
            
            #obtener las líneas del asiento que son líneas de impuesto (las que tienen tax_line_id).
            tax_lines = move.line_ids.filtered(lambda line: line.tax_line_id)
            #obtener las líneas consideradas base para el impuesto (sobre esas líneas se calcula la base imponible )
            base_lines = move.line_ids.filtered(lambda line: line.display_type == 'product')

            # Si hay impuestos, recalculamos
            if tax_lines and base_lines:
                # Por cada línea de impuesto, recalculamos el monto en moneda de compañía
                for tax_line in tax_lines:
                    # buscar las líneas base que tienen aplicado ese mismo impuesto
                    related_base_lines = base_lines.filtered(lambda line: tax_line.tax_line_id in line.tax_ids)
                    if related_base_lines:
                        # La base total en moneda de compañía para este impuesto
                        base_balance = sum(related_base_lines.mapped('balance'))
                        # Calcular el impuesto en moneda de compañía
                        tax_amount_company = base_balance * (tax_line.tax_line_id.amount / 100.0)
                        # Convertir a moneda de factura
                        tax_amount_foreign = tax_amount_company * move.invoice_currency_rate

                        # Actualizar la línea de impuesto
                        tax_line.write({
                            'balance': tax_amount_company,
                            'amount_currency': tax_amount_foreign,
                        })

        """corrigimos la fuente (las líneas) y dejamos que el motor nativo haga el resto."""
        # Ahora llamamos al super para que recalcule los totales
        super()._compute_amount()