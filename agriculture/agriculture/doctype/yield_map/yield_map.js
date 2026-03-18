frappe.ui.form.on('Yield Map', {
	refresh: function(frm) {
		if (frm.doc.land_unit) {
			frm.trigger('render_yield_map');
		}
	},
	render_yield_map: function(frm) {
		frappe.db.get_doc('Land Unit', frm.doc.land_unit).then(lu => {
			if (!lu.gps_coordinates) return;

			let coords;
			try {
				coords = JSON.parse(lu.gps_coordinates).features[0].geometry.coordinates;
			} catch (e) {
				return;
			}

			const map_id = `yield-map-${frm.doc.name}`;
			frm.fields_dict.map_html.$wrapper.html(`
				<div id="${map_id}" style="height: 400px; width: 100%; border-radius: 8px;"></div>
				<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
				<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
			`);

			setTimeout(() => {
				const map = L.map(map_id).setView([coords[1], coords[0]], 15);
				L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
					attribution: '\u00a9 OpenStreetMap'
				}).addTo(map);

				// Circle marker representing yield intensity
				const radius = Math.min(frm.doc.total_harvest_qty / 10, 500); // Scale qty to radius
				L.circle([coords[1], coords[0]], {
					color: 'green',
					fillColor: '#28a745',
					fillOpacity: 0.5,
					radius: radius > 0 ? radius : 100
				}).addTo(map)
				.bindPopup(`<b>${lu.land_unit_name}</b><br>Yield: ${frm.doc.total_harvest_qty} units<br>Acre Yield: ${frm.doc.yield_per_acre || 'N/A'}`);
			}, 500);
		});
	}
});
