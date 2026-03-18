frappe.ui.form.on('Land Unit', {
	refresh: function(frm) {
		if (frm.doc.gps_coordinates) {
			frm.trigger('render_map');
		} else {
			frm.fields_dict.map_html.$wrapper.html('<div class="alert alert-info">Enter GPS coordinates to view the map.</div>');
		}
	},
	render_map: function(frm) {
		let coords;
		try {
			coords = JSON.parse(frm.doc.gps_coordinates).features[0].geometry.coordinates;
		} catch (e) {
			return;
		}

		const map_id = `map-${frm.doc.name}`;
		frm.fields_dict.map_html.$wrapper.html(`
			<div id="${map_id}" style="height: 300px; width: 100%; border-radius: 8px;"></div>
			<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
			<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
		`);

		setTimeout(() => {
			const map = L.map(map_id).setView([coords[1], coords[0]], 15);
			L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
				maxZoom: 19,
				attribution: '\u00a9 OpenStreetMap'
			}).addTo(map);
			L.marker([coords[1], coords[0]]).addTo(map)
				.bindPopup(frm.doc.land_unit_name)
				.openPopup();
		}, 500);
	}
});
