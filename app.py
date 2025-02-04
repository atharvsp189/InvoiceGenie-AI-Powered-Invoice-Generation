import os

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json

import streamlit as st
from pprint import pprint

st.set_page_config(page_title="Invoice-Exctarctor")
st.header("Invoices Extractor")

from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize Groq LLM
llm = ChatGroq(
    model_name="mixtral-8x7b-32768",
    temperature=0.5
)

# Define the expected JSON structure
parser = JsonOutputParser(pydantic_object={
    "type": "object",
    "properties": {
        
    }
})

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant which helps to extract the order details from email and turn it into a JSON file. Extract invoice details such as name, address, city, order value, etc., and give it in a JSON file. Keep the output structure as this only.

    <output_keys>
        requestor_details.name
        requestor_details.department
        requestor_details.reason
        requestor_details.domain
        identifying_information.supplier_name
        identifying_information.gstin_number
        identifying_information.gst_rate
        identifying_information.address.street_address
        identifying_information.address.city
        identifying_information.address.state
        identifying_information.address.postal_code
        identifying_information.address.country_code
        identifying_information.contact.name
        identifying_information.contact.email_id
        identifying_information.contact.email_id_finance
        identifying_information.contact.phone_number
        identifying_information.pan_no
        identifying_information.msme_registration_no
        identifying_information.hsn_sac_code
        identifying_information.supplier_type
        local_vendor_account_information.beneficiary_account_name
        local_vendor_account_information.payment_currency
        local_vendor_account_information.bank_name
        local_vendor_account_information.ifsc_code
        local_vendor_account_information.account_type
        local_vendor_account_information.beneficiary_account_number
        local_vendor_account_information.bank_routing_method
        local_vendor_account_information.remittance_email
        foreign_currency_vendor_account_information.beneficiary_account_name
        foreign_currency_vendor_account_information.payment_currency
        foreign_currency_vendor_account_information.bank_name
        foreign_currency_vendor_account_information.account_type
        foreign_currency_vendor_account_information.swift_code
        foreign_currency_vendor_account_information.iban_no
        foreign_currency_vendor_account_information.bank_routing_method
        foreign_currency_vendor_account_information.intermediary_bank_routing_method
        foreign_currency_vendor_account_information.intermediary_swift_no
        foreign_currency_vendor_account_information.intermediary_bank_name
        foreign_currency_vendor_account_information.remittance_email
    </output_keys>
    """),
    ("user", "{input}")
])


# Create the chain that guarantees JSON output
chain = prompt | llm | parser

def parse_mail(mail: str) -> dict:
    result = chain.invoke({"input": mail})
    return json.dumps(result, indent=2)

mail = st.text_input("Enter Email/Text Invoice")

submit = st.button("Extract")

if submit:
    response = parse_mail(mail)
    pprint(response)
    # st.json(response, expanded=True)
    st.json(response)


# Example Email
# Subject: Purchase Order for Raw Materials – ABC Suppliers Pvt. Ltd

# Dear XYZ,

# I hope this email finds you well. We are reaching out to place an order for raw materials and require the necessary details for vendor registration. Kindly find the order details and required information below:

# Requestor’s Details:

# Requestor’s Name & Department: John Doe, Procurement Team

# Reason: New Vendor Registration & Raw Material Order

# Domain: Manufacturing

# Identifying Information:

# Supplier Name: ABC Suppliers Pvt. Ltd.

# GSTIN Number/Tax Registration No.: 27ABCDE1234F1Z5

# GST Rate: 18%

# Address: 123 Industrial Area, Mumbai, Maharashtra, India

# State: Maharashtra

# City: Mumbai

# Postal Code: 400001

# Country Code/Contact No.: +91 9876543210

# Contact Person Name: Mr. Rajesh Verma

# Email ID: contact@abcsuppliers.com

# Email ID Finance: finance@abcsuppliers.com

# PAN No. (For India only): ABCDE1234F

# MSME Registration No. (For India only): 12345678

# HSN/SAC Code (For India only): 7207

# GL Allocation: Manufacturing Cost

# Sub A/c: Raw Material Expenses

# Cost Center: Production Unit 1

# Supplier Type: Raw Material Vendor

# Local Vendor Account Information:

# Beneficiary Account Name: ABC Suppliers Pvt. Ltd.

# Payment Currency: INR

# Bank Name: HDFC Bank

# IFSC Code/Swift Code: HDFC0000123

# Account Type: Current

# Beneficiary Account No.: 123456789012

# BSB Number/Branch Code (For Local Vendors): 01234

# Beneficiary Bank Routing Method: NEFT/RTGS

# Remittance Email: payments@abcsuppliers.com

# Foreign Currency Vendor Account Information (If applicable):

# Beneficiary Account Name: XYZ Suppliers Pvt. Ltd.

# Payment Currency: USD

# Bank Name: Citibank NA

# Acct Type: Business

# Swift Code: CITIUS33

# IBAN No./Bank Account: US1234567890

# Beneficiary Bank Routing Method: SWIFT

# Intermediary Bank Routing Method: SWIFT

# Intermediary SWIFT No.: INTERUS33

# Intermediary Bank Name: JPMorgan Chase

# Remittance Email: finance@abcsuppliers.com

# Please confirm the receipt of this order and share the estimated delivery schedule at your earliest convenience. Additionally, we request you to send a copy of the invoice and banking details on the company letterhead for verification.

# For any clarifications, feel free to contact me at [Your Email] or +91 9876543210.

# Looking forward to your prompt response.

# Best regards,John DoeProcurement TeamXYZ Manufacturing Pvt. Ltd.Email: john.doe@xyzmanufacturing.comPhone: +91 9876543210