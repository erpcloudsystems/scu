import frappe
from frappe import _


@frappe.whitelist()
def on_change(doc, method=None):
    if frappe.db.exists("Subscription Invoice", {"parent": doc.name}):
        invoices = frappe.db.get_list(
            "Subscription Invoice", {"parent": doc.name}, ["invoice"]
        )
        current = invoices[-1]["invoice"]
        if not frappe.db.exists("Payment Request", {"reference_name": current}):
            # sales_invoice = frappe.get_doc("Sales Invoice", current)
            domain_name = frappe.db.get_value(
                "Domain Name", {"domain_request": doc.domain_request}, ["name"]
            )
            frappe.db.set_value(
                "Sales Invoice",
                current,
                "domain_name",
                domain_name,
                update_modified=True,
            )
            # sales_invoice.domain_name = domain_name
            # sales_invoice.save()
            invoice = frappe.db.get_list(
                "Sales Invoice", {"name": current}, ["customer"]
            )
            email_to = frappe.db.get_value(
                "Customer", {"name": invoice[-1]["customer"]}, ["email_id"]
            )
            grand_total = frappe.db.get_list(
                "Sales Invoice", {"name": current}, ["grand_total"]
            )
            currency = frappe.db.get_list(
                "Sales Invoice", {"name": current}, ["currency"]
            )
            contact_person = frappe.db.get_list(
                "Sales Invoice", {"name": current}, ["contact_person"]
            )
            posting_date = frappe.db.get_list(
                "Sales Invoice", {"name": current}, ["posting_date"]
            )
            payment_request = frappe.get_doc(
                {
                    "doctype": "Payment Request",
                    "payment_request_type": "Inward",
                    "transaction_date": posting_date[-1]["posting_date"],
                    "mode_of_payment": "Bank Draft",
                    "party_type": "Customer",
                    "reference_doctype": "Sales Invoice",
                    "reference_name": current,
                    "party": invoice[-1]["customer"],
                    "grand_total": grand_total[-1]["grand_total"],
                    "currency": currency[-1]["currency"],
                    "print_format": "Standard",
                    "email_to": email_to,
                    "subscription": doc.name,
                    "subject": "Payment Request for {invoice_id}".format(
                        invoice_id=current
                    ),
                    "message": """
                Dear {contact_person},
                Requesting payment for {doctype}, {name} for {grand_total}.
                Please reply with payment receipt or login to portal and upload the required documents 
                """.format(
                        contact_person=contact_person[-1]["contact_person"],
                        doctype="Sales Invoice",
                        name=current,
                        grand_total=grand_total[-1]["grand_total"],
                    ),
                }
            )
            payment_request.insert()
            payment_request.submit()
            frappe.db.commit()
            resend_payment_email(payment_request.name)


@frappe.whitelist(allow_guest=True)
def resend_payment_email(docname):
    return frappe.get_doc("Payment Request", docname).send_email()

