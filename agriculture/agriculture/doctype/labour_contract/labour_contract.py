# Copyright (c) 2026, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class LabourContract(Document):
	@frappe.whitelist()
	def make_journal_entry(self):
		if self.journal_entry:
			frappe.throw(_("Journal Entry already exists: {0}").format(self.journal_entry))
		
		if not self.total_wage_bill:
			frappe.throw(_("Total Wage Bill is zero. Cannot create Journal Entry."))

		# Create Journal Entry (simplified example)
		# Debit: Agriculture Expense (or from settings)
		# Credit: Cash/Bank
		
		# For this implementation, we link it to the Crop Cycle Project if available
		project = None
		if self.crop_cycle:
			project = frappe.db.get_value("Crop Cycle", self.crop_cycle, "project")

		je = frappe.get_doc({
			"doctype": "Journal Entry",
			"posting_date": frappe.utils.nowdate(),
			"user_remark": f"Wage bill for {self.contract_name}",
			"accounts": [
				{
					"account": "Expenses - Agriculture - CP", # Hardcoded placeholder, should ideally be from Settings
					"debit_in_account_currency": self.total_wage_bill,
					"project": project
				},
				{
					"account": "Cash - CP", # Hardcoded placeholder
					"credit_in_account_currency": self.total_wage_bill
				}
			]
		})
		je.insert()
		self.journal_entry = je.name
		self.save()
		return je.name
