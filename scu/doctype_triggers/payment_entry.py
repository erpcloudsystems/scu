import frappe
from frappe import _


@frappe.whitelist()
def on_submit(doc, method=None):
    sales_invoice = frappe.db.get_value(
        "Payment Entry Reference", {"parent": doc.name}, "reference_name"
    )
    domain_exist = frappe.db.exists(
        "Sales Invoice", {"name": sales_invoice}, "domain_name"
    )
    if domain_exist:
        domain_name = frappe.db.get_value(
            "Sales Invoice", {"name": sales_invoice}, "domain_name"
        )
        domain = frappe.get_doc("Domain Name", domain_name)
        domain.status = "Pending"
        domain.save()

