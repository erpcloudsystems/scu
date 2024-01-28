// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Domain Status and Near Expire"] = {
	"filters": [
	{
		label: __("Expires After"),
		fieldname: "expires_after",
		fieldtype: "Select",
		options: [
			"",
			{ "value": 1, "label": __("One Month") },
			{ "value": 2, "label": __("Two Month") },
			{ "value": 3, "label": __("Three Month") },
			{ "value": 4, "label": __("Four Month") },
			{ "value": 6, "label": __("Five Month") },
		],
	},
	{
		label: __("Status"),
		fieldname: "status",
		fieldtype: "Select",
		options: [
			"",
			{ "value": "new", "label": __("New") },
			{ "value": "Active", "label": __("Active") },
			{ "value": "Disabled", "label": __("Disabled") },
			{ "value": "Pending", "label": __("Pending") },
			{ "value": "Suspended", "label": __("Suspended") },
		],
	},
	{
		label: __("Extension"),
		fieldname: "extension",
		fieldtype: "Select",
		options: [
			"",
			{ "value": ".eg", "label": __(".eg") },
			{ "value": ".edu.eg", "label": __(".edu.eg") },
			{ "value": ".com.eg", "label": __(".com.eg") },
			{ "value": ".gov.eg", "label": __(".gov.eg") },
			{ "value": ".net.eg", "label": __(".net.eg") },
			{ "value": ".name.eg", "label": __(".name.eg") },
			{ "value": ".org.eg", "label": __(".org.eg") },
			{ "value": ".sci.eg", "label": __(".sci.eg") },
			{ "value": ".edu.eg", "label": __(".edu.eg") },
			{ "value": ".eun.eg", "label": __(".eun.eg") },
			{ "value": ".gov.eg", "label": __(".gov.eg") },
			{ "value": ".mil.eg", "label": __(".mil.eg") },
			{ "value": ".sci.eg", "label": __(".sci.eg") },
		],
	},

{
	fieldname: "from_date",
	label: __("From Date"),
				fieldtype: "Date",


},
{
	fieldname:"to_date",
	label: __("To Date"),
				fieldtype: "Date",

},
]
};

