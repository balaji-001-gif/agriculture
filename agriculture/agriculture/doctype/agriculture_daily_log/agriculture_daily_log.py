# Copyright (c) 2026, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from agriculture.agriculture.stock_utility import create_stock_entry_for_input

class AgricultureDailyLog(Document):
	def on_submit(self):
		create_stock_entry_for_input(self)
