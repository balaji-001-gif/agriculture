# Copyright (c) 2026, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{"label": _("Land Unit"), "fieldname": "land_unit", "fieldtype": "Link", "options": "Land Unit", "width": 150},
		{"label": _("Total Fuel Used (L)"), "fieldname": "total_fuel", "fieldtype": "Float", "width": 120},
		{"label": _("Total Labour Hours"), "fieldname": "total_labour", "fieldtype": "Float", "width": 120},
		{"label": _("Total Irrigation Time (Min)"), "fieldname": "total_irrigation", "fieldtype": "Float", "width": 150},
		{"label": _("Fuel per Acre"), "fieldname": "fuel_per_acre", "fieldtype": "Float", "width": 120},
		{"label": _("Labour per Acre"), "fieldname": "labour_per_acre", "fieldtype": "Float", "width": 120}
	]

def get_data(filters):
	data = []
	land_units = frappe.get_all("Land Unit", fields=["name", "area"])
	
	for lu in land_units:
		# Fuel from Equipment Logs
		fuel = frappe.db.get_value("Equipment Log", {"land_unit": lu.name, "docstatus": 1}, "sum(fuel_consumed)") or 0
		
		# Labour Hours from Labour contracts
		# (Labour Contract child table rows filtered by land_unit)
		labour = frappe.db.sql("""
			SELECT sum(child.hours_worked) 
			FROM `tabLabour Attendance` child 
			JOIN `tabLabour Contract` parent ON child.parent = parent.name 
			WHERE parent.land_unit = %s
		""", lu.name)[0][0] or 0
		
		# Irrigation duration
		irrigation = frappe.db.get_value("Irrigation Schedule", {"land_unit": lu.name, "status": "Completed"}, "sum(duration_mins)") or 0
		
		area = float(lu.area or 1)
		
		data.append({
			"land_unit": lu.name,
			"total_fuel": fuel,
			"total_labour": labour,
			"total_irrigation": irrigation,
			"fuel_per_acre": fuel / area,
			"labour_per_acre": labour / area
		})
	
	return data
