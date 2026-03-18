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
		{"label": _("Crop Cycle"), "fieldname": "crop_cycle", "fieldtype": "Link", "options": "Crop Cycle", "width": 150},
		{"label": _("Land Unit"), "fieldname": "land_unit", "fieldtype": "Link", "options": "Land Unit", "width": 150},
		{"label": _("Revenue"), "fieldname": "revenue", "fieldtype": "Currency", "width": 120},
		{"label": _("Labour Cost"), "fieldname": "labour_cost", "fieldtype": "Currency", "width": 120},
		{"label": _("Fuel Cost"), "fieldname": "fuel_cost", "fieldtype": "Currency", "width": 120},
		{"label": _("Material Cost"), "fieldname": "material_cost", "fieldtype": "Currency", "width": 120},
		{"label": _("Total Cost"), "fieldname": "total_cost", "fieldtype": "Currency", "width": 120},
		{"label": _("Net Profit"), "fieldname": "net_profit", "fieldtype": "Currency", "width": 120}
	]

def get_data(filters):
	data = []
	crop_cycles = frappe.get_all("Crop Cycle", fields=["name", "land_unit", "project"])
	
	for cc in crop_cycles:
		# Revenue from Sales Invoice Items linked to Project
		revenue = frappe.db.get_value("Sales Invoice Item", {"project": cc.project, "docstatus": 1}, "sum(base_net_amount)") or 0
		
		# Labour Cost from Labour Contracts linked to Crop Cycle
		labour_cost = frappe.db.get_value("Labour Contract", {"crop_cycle": cc.name}, "sum(total_wage_bill)") or 0
		
		# Material Cost (Stock Entry - Material Issue)
		material_cost = frappe.db.get_value("Stock Entry Detail", {"project": cc.project, "docstatus": 1, "t_warehouse": ["is", "not set"]}, "sum(base_amount)") or 0
		
		# Fuel Cost (can be estimated from Equipment Logs or specific item category)
		# For simplicity, we filter Stock Entry items with category 'Fuel' if available, or just a placeholder logic
		fuel_cost = 0 # In a real system, we'd link this more specifically
		
		total_cost = labour_cost + material_cost + fuel_cost
		net_profit = revenue - total_cost
		
		data.append({
			"crop_cycle": cc.name,
			"land_unit": cc.land_unit,
			"revenue": revenue,
			"labour_cost": labour_cost,
			"fuel_cost": fuel_cost,
			"material_cost": material_cost,
			"total_cost": total_cost,
			"net_profit": net_profit
		})
	
	return data
