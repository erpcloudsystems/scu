# Copyright (c) 2022, ERPCloud.Systems and contributors
# For license information, please see license.txt

import frappe
from frappe import _

from frappe.utils import flt
from frappe.utils import add_to_date
import datetime


def execute(filters=None):
    columns = get_columns(filters)
    data = get_data(filters)
    return columns, data


def get_columns(filters):
    columns = [
        {
            "label": _("Name"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options":"Domain Name",
            "width": 110,
        },
        {
            "label": _("Domain name"),
            "fieldname": "domain_name",
            "fieldtype": "Data",
            "width": 140,
        },
        {
            "label": _("Extension"),
            "fieldname": "extension",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("Status"),
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("Primary name server"),
            "fieldname": "primary_name_server",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("Secondary name server"),
            "fieldname": "secondary_name_server",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("End Date"),
            "fieldname": "end_date",
            "fieldtype": "Date",
            "width": 110,
        },
    ]
    return columns


def get_conditions(filters):
    conditions = ""
    if filters.get("status"):
        conditions += " AND domain_name.status=%s" % frappe.db.escape(
            filters.get("status")
        )
    if filters.get("expires_after"):
        expires_after = int(filters.get("expires_after"))
        now = datetime.datetime.today().strftime("%Y-%m-%d")
        end_date = add_to_date(now, months=-expires_after)
        conditions += (
            " AND domain_name.end_date BETWEEN  '{expire_data}' and '{today}' ".format(
                expire_data=end_date, today=now
            )
        )
    if filters.get("extension"):
        conditions += " AND domain_name.extension=%s" % frappe.db.escape(
            filters.get("extension")
        )
    if filters.get("from_date"):
        conditions += " AND domain_name.end_date>='%s'" % filters.get("from_date")

    if filters.get("to_date"):
        conditions += " AND domain_name.end_date<='%s'" % filters.get("to_date")

    return conditions


def get_data(filters):
    conditions = get_conditions(filters)
    query = get_query(conditions)

    ingaze_row = []

    for record in query:
        # fetch material records linked to the purchase order item
        # mr_record = mr_records.get(records.material_request_item, [{}])[0]
        row_detail = {
            "name": record.name,
            "domain_name": record.domain_name,
            "extension": record.extension,
            "status": record.status,
            "primary_name_server": record.primary_name_server,
            "secondary_name_server": record.secondary_name_server,
            "end_date": record.end_date,
        }
        ingaze_row.append(row_detail)
    return ingaze_row


def get_query(conditions):
    return frappe.db.sql(
        """
        SELECT 
             domain_name.name AS name,
            domain_name.domain_name AS domain_name,
            domain_name.extension AS extension,
            domain_name.status AS status,
            domain_name.primary_name_server AS primary_name_server,
            domain_name.secondary_name_server AS secondary_name_server,
            domain_name.end_date AS end_date
        FROM `tabDomain Name` domain_name
        
        WHERE 1 =  1
        {conditions}
        """.format(
            conditions=conditions
        ),
        as_dict=1,
    )  # nosec


def license_details():
    return frappe._dict(
        frappe.db.sql(
            """
        SELECT 
            domain_name.parent AS domain_name_parent,
             vehicle_license.name AS vehicle_license_name

        FROM `tabLicense Entry Summary` domain_name
        JOIN `tabVehicle License` vehicle_license ON vehicle_license.name = domain_name.parent
        WHERE vehicle_license.docstatus =  1
        """
        )
    )  # nosec


def domain_name():
    return frappe._dict(
        frappe.db.sql(
            """
        SELECT 
            domain_name_item.sales_order AS against_sales_order,
             domain_name.name AS domain_name_name

        FROM `tabSales Invoice` domain_name
        JOIN `tabSales Invoice Item` domain_name_item ON domain_name.name = domain_name_item.parent
        WHERE domain_name.status != "Cancelled"
        """
        )
    )  # nosec

