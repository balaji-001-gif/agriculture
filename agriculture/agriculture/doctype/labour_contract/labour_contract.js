frappe.ui.form.on('Labour Contract', {
	refresh: function(frm) {
		if (frm.doc.status === 'Active' && !frm.doc.journal_entry) {
			frm.add_custom_button(__('Create Journal Entry'), () => {
				frm.call('make_journal_entry');
			});
		}
	}
});

frappe.ui.form.on('Labour Attendance', {
	hours_worked: function(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		if (row.hours_worked && row.pay_rate) {
			frappe.model.set_value(cdt, cdn, 'total_pay', row.hours_worked * row.pay_rate);
			calculate_contract_totals(frm);
		}
	},
	pay_rate: function(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		if (row.hours_worked && row.pay_rate) {
			frappe.model.set_value(cdt, cdn, 'total_pay', row.hours_worked * row.pay_rate);
			calculate_contract_totals(frm);
		}
	},
	attendance_remove: function(frm) {
		calculate_contract_totals(frm);
	}
});

function calculate_contract_totals(frm) {
	let total_hours = 0;
	let total_wage = 0;
	(frm.doc.attendance || []).forEach(row => {
		total_hours += flt(row.hours_worked);
		total_wage += flt(row.total_pay);
	});
	frm.set_value('total_hours', total_hours);
	frm.set_value('total_wage_bill', total_wage);
}
