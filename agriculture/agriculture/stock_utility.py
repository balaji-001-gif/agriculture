# Copyright (c) 2026, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def create_stock_entry_for_input(doc):
    """
    Creates a Stock Entry (Material Issue) for inputs recorded in Daily Log.
    """
    if not doc.issue_from_stock or doc.stock_entry:
        return

    if not doc.warehouse:
        frappe.throw(_("Please specify a Warehouse to issue stock from."))

    # In a real scenario, we would determine the item from the activity (pesticide/fertilizer)
    # For this implementation, we'll assume the user might have specified an item in the log
    # or we fetch the default item linked to the activity type.
    
    # Placeholder: Assuming we add an 'item' field to the Daily Log or use a linked doctype
    # For now, let's just implement the logic structure.
    
    stock_entry = frappe.get_doc({
        "doctype": "Stock Entry",
        "stock_entry_type": "Material Issue",
        "company": frappe.db.get_default("company"),
        "from_warehouse": doc.warehouse,
        "items": [
            {
                "item_code": doc.item, # We need to add this field to Daily Log
                "qty": doc.qty_used,   # We need to add this field to Daily Log
                "uom": doc.uom,        # We need to add this field to Daily Log
                "warehouse": doc.warehouse
            }
        ]
    })
    
    stock_entry.insert()
    stock_entry.submit()
    
    doc.db_set("stock_entry", stock_entry.name)
    frappe.msgprint(_("Stock Entry {0} created for input usage.").format(stock_entry.name))
