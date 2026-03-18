# Copyright (c) 2026, Administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate
import requests

class WeatherLog(Document):
	pass

@frappe.whitelist()
def fetch_weather_data(land_unit):
	"""
	Fetches weather data for a Land Unit.
	Uses Geolocation coordinates if available.
	"""
	lu = frappe.get_doc("Land Unit", land_unit)
	if not lu.gps_coordinates:
		return
	
	# coordinates are stored as a GeoJSON string in Geolocation field
	import json
	try:
		coords = json.loads(lu.gps_coordinates).get("features")[0].get("geometry").get("coordinates")
		lon, lat = coords[0], coords[1]
	except Exception:
		return

	api_key = frappe.db.get_single_value("Agriculture Settings", "openweathermap_api_key")
	if not api_key:
		return

	url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
	response = requests.get(url)
	if response.status_code == 200:
		data = response.json()
		return {
			"temperature": data.get("main", {}).get("temp"),
			"humidity": data.get("main", {}).get("humidity"),
			"wind_speed": data.get("wind", {}).get("speed"),
			"weather_condition": data.get("weather", [{}])[0].get("main"),
			"precipitation": data.get("rain", {}).get("1h", 0)
		}

def update_weather_daily():
	"""Scheduled task to update weather for all Land Units"""
	land_units = frappe.get_all("Land Unit", filters={"gps_coordinates": ["is", "set"]})
	for lu in land_units:
		weather_data = fetch_weather_data(lu.name)
		if weather_data:
			frappe.get_doc({
				"doctype": "Weather Log",
				"land_unit": lu.name,
				"date": nowdate(),
				**weather_data,
				"source": "OpenWeatherMap"
			}).insert(ignore_permissions=True)
