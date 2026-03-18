import frappe
from frappe.model.document import Document
from frappe import _

class EquipmentLog(Document):
	def validate(self):
		if self.starting_odometer and self.ending_odometer:
			if self.ending_odometer < self.starting_odometer:
				frappe.throw(_("Ending Odometer cannot be less than Starting Odometer"))

	def on_submit(self):
		if self.fuel_item and self.fuel_consumed:
			self.create_fuel_stock_entry()

	def create_fuel_stock_entry(self):
		# Default warehouse - ideally from settings, using 'Stores' as common ERPNext default
		warehouse = frappe.db.get_single_value("Agriculture Settings", "fuel_warehouse") or "Stores - CP"
		
		# Link to Project from Crop Cycle
		project = frappe.db.get_value("Crop Cycle", self.crop_cycle, "project")

		se = frappe.get_doc({
			"doctype": "Stock Entry",
			"stock_entry_type": "Material Issue",
			"company": frappe.defaults.get_defaults().company,
			"items": [
				{
					"item_code": self.fuel_item,
					"qty": self.fuel_consumed,
					"s_warehouse": warehouse,
					"project": project
				}
			]
		})
		se.insert()
		se.submit()
		self.db_set("stock_entry", se.name)
