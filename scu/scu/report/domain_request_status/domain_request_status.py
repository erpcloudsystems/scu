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
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("Workflow State"),
            "fieldname": "workflow_state",
            "fieldtype": "Data",
            "width": 140,
        },
        {
            "label": _("Company Name"),
            "fieldname": "company_name",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("Domain Name"),
            "fieldname": "domain_name",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": _("Registrar Type"),
            "fieldname": "registrar_type",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("Extension"),
            "fieldname": "extension",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("Profile Type"),
            "fieldname": "profile_type",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("Organization Name"),
            "fieldname": "organization_name",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("Complete Domain Name"),
            "fieldname": "complete_domain_name",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("Primary Server Hostname"),
            "fieldname": "primary_server_hostname",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("Primary Server Netaddress"),
            "fieldname": "primary_server_netaddress",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("Secondary Server Hostname"),
            "fieldname": "secondary_server_hostname",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("Secondary Server Netaddress"),
            "fieldname": "secondary_server_netaddress",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("ISP Name"),
            "fieldname": "isp_name",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("Subscription Plan"),
            "fieldname": "subscription_plan",
            "fieldtype": "Data",
            "width": 110,
        },
        {
            "label": _("Subscription Period"),
            "fieldname": "subscription_period",
            "fieldtype": "Data",
            "width": 110,
        },
    ]
    return columns


def get_conditions(filters):
    conditions = ""
    if filters.get("status"):
        conditions += " AND domain_request.workflow_state=%s" % frappe.db.escape(
            filters.get("status")
        )
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
            "workflow_state": record.workflow_state,
            "company_name": record.company_name,
            "domain_name": record.domain_name,
            "registrar_type": record.registrar_type,
            "extension": record.extension,
            "profile_type": record.profile_type,
            "organization_name": record.organization_name,
            "complete_domain_name": record.complete_domain_name,
            "primary_server_hostname": record.primary_server_hostname,
            "primary_server_netaddress": record.primary_server_netaddress,
            "secondary_server_hostname": record.secondary_server_hostname,
            "secondary_server_netaddress": record.secondary_server_netaddress,
            "isp_name": record.isp_name,
            "subscription_plan": record.subscription_plan,
            "subscription_period": record.subscription_period,
        }
        ingaze_row.append(row_detail)
    return ingaze_row


def get_query(conditions):
    return frappe.db.sql(
        """
        SELECT 
             domain_request.name AS name,
            domain_request.workflow_state AS workflow_state,
            domain_request.company_name AS company_name,
            domain_request.domain_name AS domain_name,
            domain_request.registrar_type AS registrar_type,
            domain_request.extension AS extension,
            domain_request.profile_type AS profile_type,
            domain_request.organization_name AS organization_name,
            domain_request.complete_domain_name AS complete_domain_name,
            domain_request.primary_server_hostname AS primary_server_hostname,
            domain_request.primary_server_netaddress AS primary_server_netaddress,
            domain_request.secondary_server_hostname AS secondary_server_hostname,
            domain_request.secondary_server_netaddress AS secondary_server_netaddress,
            domain_request.isp_name AS isp_name,
            domain_request.subscription_plan AS subscription_plan,
            domain_request.subscription_period AS subscription_period
        FROM `tabDomain Request` domain_request
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

