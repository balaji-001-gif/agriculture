# Copyright (c) 2026, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import today, get_link_to_form

def send_daily_agricultural_alerts():
	"""
	Scheduled task to send notifications for pending agricultural tasks.
	"""
	pending_tasks = frappe.get_all("Task", 
		filters={
			"status": ["not in", ["Completed", "Cancelled"]],
			"exp_start_date": ["<=", today()]
		},
		fields=["name", "subject", "project", "exp_start_date"]
	)

	if not pending_tasks:
		return

	# Group tasks by project (which represents a Crop Cycle)
	tasks_by_project = {}
	for task in pending_tasks:
		if task.project not in tasks_by_project:
			tasks_by_project[task.project] = []
		tasks_by_project[task.project].append(task)

	for project, tasks in tasks_by_project.items():
		# Find the Crop Cycle linked to this project
		crop_cycle = frappe.db.get_value("Crop Cycle", {"project": project}, "name")
		if not crop_cycle:
			continue

		# Prepare message
		message = _("You have {0} pending agricultural tasks for Crop Cycle {1}:").format(len(tasks), crop_cycle)
		message += "\n\n"
		for task in tasks:
			message += "- {0} ({1})\n".format(task.subject, task.name)

		# Send notification to Agriculture Users and Managers
		users = frappe.get_all("User", filters={"enabled": 1}, fields=["name"]) # In a real scenario, we'd filter by Role
		
		# For demonstration, we'll use frappe.msgprint for the current user 
		# but in a background job, we'd use frappe.sendmail or System Notifications
		
		for user in users:
			if "Agriculture User" in frappe.get_roles(user.name) or "Agriculture Manager" in frappe.get_roles(user.name):
				frappe.get_doc({
					"doctype": "Notification Log",
					"for_user": user.name,
					"subject": _("Daily Agricultural Alert"),
					"email_content": message,
					"document_type": "Crop Cycle",
					"document_name": crop_cycle
				}).insert(ignore_permissions=True)

	frappe.db.commit()
