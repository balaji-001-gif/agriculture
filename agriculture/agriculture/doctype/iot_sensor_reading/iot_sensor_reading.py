# Copyright (c) 2026, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class IoTSensorReading(Document):
	pass

@frappe.whitelist(allow_guest=True)
def ingest_telemetry(sensor_id, temperature=None, humidity=None, soil_moisture=None, lux=None, battery=None):
	"""
	API Endpoint for IoT sensors to POST data.
	Example: /api/method/agriculture.agriculture.doctype.iot_sensor_reading.iot_sensor_reading.ingest_telemetry
	"""
	# Find land unit associated with sensor (simple mapping for now)
	# In a real system, we'd have a 'Sensor' DocType linked to Land Unit
	land_unit = frappe.db.get_value("Land Unit", {"land_unit_name": ["like", f"%{sensor_id}%"]}, "name")

	doc = frappe.get_doc({
		"doctype": "IoT Sensor Reading",
		"sensor_id": sensor_id,
		"land_unit": land_unit,
		"temperature": temperature,
		"humidity": humidity,
		"soil_moisture": soil_moisture,
		"light_intensity": lux,
		"battery_level": battery
	})
	doc.insert(ignore_permissions=True)
	return {"status": "success", "name": doc.name}
