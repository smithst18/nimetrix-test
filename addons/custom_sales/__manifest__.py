{
    "name": "Custom Sales Nimetrix",
    "version": "1.0",
    "description": "Modulo Custom para Sales odoo 18 prueba tecnica Nimetrix",
    "summary": "",
    "author": "E.A.A",
    "website": "",
    "license": "LGPL-3",
    "category": "",
    "depends": [
        "sale_management",
        "stock"
    ],
    "data": [
        #security
        "security/groups.xml",
        "security/admin/ir.model.access.csv",
        "security/ir.model.access.csv",
        # views
        "views/custom_sale_order.xml",
        "views/report_pending_dispatch_view.xml",
        #wizards
        "wizards/views/confirm_order.xml",
    ],
    "demo": [],
    "auto_install": False,
    "application": False,
    'installable': True,
    "assets": {},
}
