// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Domain Request Status"] = {
		"filters": [
	{
		label: __("Status"),
		fieldname: "status",
		fieldtype: "Select",
		options: [
			"",
			{ "value": "Pending", "label": __("Pending") },
			{ "value": "Returned To Customer", "label": __("Returned To Customer") },
			{ "value": "New Request", "label": __("New Request") },
			{ "value": "Approved", "label": __("Approved") },
			{ "value": "Rejected", "label": __("Rejected") },
		],
	},
	
]
};

