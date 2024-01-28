// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Domain Request', {
	subscription_plan: function(frm) {
        frm.doc.total = frm.doc.cost * frm.doc.subscription_period
        frm.refresh()
	},
    subscription_period: function(frm) {
        frm.doc.total = frm.doc.cost * frm.doc.subscription_period
        frm.refresh()
	}
});
