import frappe
from frappe.model.document import Document
from frappe import _

class HarvestRecording(Document):
	def on_submit(self):
		if self.create_stock_entry:
			self.create_material_receipt()

	def create_material_receipt(self):
		"""
		Creates a Material Receipt for the harvested yield.
		"""
		# Get the crop item from the Crop Cycle
		crop_name = frappe.db.get_value("Crop Cycle", self.crop_cycle, "crop")
		item_code = frappe.db.get_value("Crop", crop_name, "name") # Assuming Crop name is item code or linked
		
		# If not direct, look for item linked to Crop
		if not frappe.db.exists("Item", item_code):
			item_code = frappe.db.get_value("Crop", crop_name, "item")
			
		if not item_code:
			frappe.throw(_("No Item linked to Crop {0}. Cannot create Stock Entry.").format(crop_name))

		stock_entry = frappe.get_doc({
			"doctype": "Stock Entry",
			"stock_entry_type": "Material Receipt",
			"company": frappe.db.get_default("company"),
			"to_warehouse": self.target_warehouse,
			"items": [
				{
					"item_code": item_code,
					"qty": self.yield_quantity,
					"uom": self.uom,
					"t_warehouse": self.target_warehouse,
					"basic_rate": 0 # User can update cost later
				}
			]
		})
		stock_entry.insert()
		stock_entry.submit()
		self.db_set("stock_entry", stock_entry.name)
