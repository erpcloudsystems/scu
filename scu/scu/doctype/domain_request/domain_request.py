# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime
from frappe.utils import add_to_date


class DomainRequest(Document):
    def on_submit(self):
        new_cusotmer = frappe.get_doc(
            {
                "doctype": "Customer",
                "customer_name": self.organization_name,
                "domain_request": self.name,
                "customer_group": self.organization_group,
                "customer_type": self.organization_type,
                "territory": self.territory,
            }
        )
        new_cusotmer.insert()
        doc = frappe.get_doc("Domain Request", self.name)
        # doc.customer = new_cusotmer.name
        doc.db_set("customer", new_cusotmer.name, update_modified=True)
        customer_name = new_cusotmer.name
        links = [
            {
                "link_doctype": "Customer",
                "link_name": customer_name,
                "link_title": customer_name,
            },
            {
                "link_doctype": "Customer",
                "link_name": customer_name,
                "link_title": customer_name,
            },
        ]

        if not self.same_as_administrative_contact:

            emails = [
                {
                    "email_id": self.email_id,
                    "is_primary": 1,
                },
                {
                    "email_id": self.administrative_email,
                    "is_primary": 0,
                },
                {
                    "email_id": self.e_mailbox,
                    "is_primary": 0,
                },
            ]
        else:
            emails = [
                {
                    "email_id": self.email_id,
                    "is_primary": 1,
                },
                {
                    "email_id": self.administrative_email,
                    "is_primary": 0,
                },
            ]
        if not self.same_as_administrative_contact:
            contacts = [
                {
                    "phone": self.administrative_phone_number,
                    "is_primary_phone": 1,
                    "is_primary_mobile_no": 1,
                },
                {
                    "phone": self.technical_phone_number,
                    "is_primary_phone": 0,
                    "is_primary_mobile_no": 0,
                },
            ]
        else:
            contacts = [
                {
                    "phone": self.administrative_phone_number,
                    "is_primary_phone": 1,
                    "is_primary_mobile_no": 1,
                }
            ]

        contact = frappe.get_doc(
            {
                "doctype": "Contact",
                "first_name": self.administrative_contact_name,
                "links": links,
                "email_ids": emails,
                "phone_nos": contacts,
                "domain_request": self.name,
                "is_primary_contact": 1,
                "is_billing_contact": 1,
                "company_name": self.administrative_organization_name,
            }
        )
        # if (
        #     kwargs["data"].get("customer_name")
        #     and kwargs["data"].get("email_id")
        #     and kwargs["data"].get("mobile_no")
        # ):

        contact.insert()
        new_cusotmer.customer_primary_contact = contact.name

        # address = frappe.new_doc("Address")
        address_link = [
            {
                "link_doctype": "Customer",
                "link_name": customer_name,
                "link_title": customer_name,
            }
        ]
        address = frappe.get_doc(
            {
                "doctype": "Address",
                "address_title": self.organization_name,
                "address_line1": self.address,
                "address_line2": self.administrative_street,
                "domain_request": self.name,
                "city": self.city,
                "country": self.territory,
                "address_type": "Billing",
                "is_primary_address_type": 1,
                "is_shipping_address_type": 1,
                "links": address_link,
            }
        )

        # address.address_title = self.organization_name
        # address.address_line1 = self.address
        # address.city = self.city
        # address.country = self.territory
        # address.address_type = "Billing"
        # address.is_primary_address_type = 1
        # address.is_shipping_address_type = 1
        # address.links = address_link

        # if (
        #     kwargs["data"].get("customer_name")
        #     and kwargs["data"].get("address_line1")
        #     and kwargs["data"].get("city")
        #     and kwargs["data"].get("address_type", "Billing")
        # ):
        address.insert()
        new_cusotmer.customer_primary_address = address.name
        new_cusotmer.save()
        # now = datetime.datetime.today()
        billing_interval = self.billing_interval
        now = datetime.datetime.today().strftime("%Y-%m-%d")
        end_date = add_to_date(
            now,
            months=int(self.subscription_period) if billing_interval == "Month" else 0,
            years=int(self.subscription_period) if billing_interval == "Year" else 0,
            days=int(self.subscription_period) if billing_interval == "Day" else 0,
        )
        domain_name = frappe.get_doc(
            {
                "doctype": "Domain Name",
                "domain_name": self.domain_name,
                "extension": self.extension,
                "domain_request": self.name,
                "status": "new",
                "primary_name_server": self.primary_server_hostname,
                "secondary_name_server": self.primary_server_hostname,
                "date": datetime.datetime.today().strftime("%Y-%m-%d"),
                "end_date": end_date,
            }
        )
        domain_name.insert()
        # doc.domain = domain_name.name
        doc.db_set("domain", domain_name.name, update_modified=True)

        # end_date = add_to_date(
        #     now,
        #     months=int(self.subscription_period) if billing_interval == "Month" else 0,
        #     years=int(self.subscription_period) if billing_interval == "Year" else 0,
        #     days=int(self.subscription_period) if billing_interval == "Day" else 0,
        # )
        d1 = datetime.datetime.strptime(now, "%Y-%m-%d")
        d2 = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        days_until_due = d2 - d1
        plans = [
            {
                "plan": self.subscription_plan,
                "qty": self.subscription_period,
            }
        ]
        subscription = frappe.get_doc(
            {
                "doctype": "Subscription",
                "party_type": "Customer",
                "domain_request": self.name,
                "party": customer_name,
                "start_date": now,
                "end_date": end_date,
                "plans": plans,
                "generate_invoice_at_period_start": 1,
            }
        )
        subscription.insert()
        doc.db_set("subscription", subscription.name, update_modified=True)
        # doc.save()
        # customer =frappe.get_doc(kwargs['data'])
        # customer.insert()
        frappe.db.commit()

    # def on_update_after_submit(self):
    #     if len(self.invoices):
    #         current = self.invoices[-1]
    #         if frappe.db.exists("Sales Invoce", current.get("invoice")):
    #             doc = frappe.get_doc("Sales Invoce", current.get("invoice"))
    #             return doc
    #         else:
    #             doc = None
    #     if doc:
    #         if not frappe.db.exists("Payment Request", {"reference_name": doc.name}):
    #             payment_request = frappe.get_doc(
    #                 {
    #                     "doctype": "Payment Request",
    #                     "payment_request_type": "inward",
    #                     "transaction_date": doc.posting_date,
    #                     "mode_of_payment": "Bank Draft",
    #                     "party_type": "Customer",
    #                     "party": self.customer or doc.customer,
    #                     "reference_doctype": " Sales Invoice",
    #                     "reference_name": doc.name,
    #                     "grand_total": doc.grand_total,
    #                     "currency": doc.currenct,
    #                     "print_format": "Standard",
    #                     "email_to": self.email_id,
    #                     "subject": "Payment Request for {invoice_id}".format(
    #                         invoice_id=doc.name
    #                     ),
    #                     "message": """
    #                 Dear {contact_person},
    #                 Requesting payment for {doctype}, {name} for {grand_total}.
    #                 Please reply with payment receipt or login to portal and upload the required documents
    #                 """.format(
    #                         contact_person=doc.contact_person,
    #                         doctype="Sales Invoice",
    #                         name=doc.name,
    #                         grand_total=doc.grand_total,
    #                     ),
    #                 }
    #             )
    #             payment_request.insert()
    #             frappe.db.commit()

