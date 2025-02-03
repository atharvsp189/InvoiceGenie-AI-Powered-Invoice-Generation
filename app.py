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

# Create a simple prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant which helps to extract the order details from email and turn it into json file. Extract Invoices details such as name, address, city, order value etc. and give it in a json file"""),
    ("user", "{input}")
])

# Create the chain that guarantees JSON output
chain = prompt | llm | parser

def parse_mail(mail: str) -> dict:
    result = chain.invoke({"input": mail})
    return json.dumps(result, indent=2)

        
# Example usage
# mail = """Subject: Purchase Order for Raw Materials
# Dear XYZ,

# I hope you are doing well. We would like to place an order for the following raw materials. Please find the details below:

# Order Details:
# Company Name: ABC Industries Pvt. Ltd.
# Billing Address: Plot No. 123, Industrial Area, Pune, Maharashtra - 411001
# Shipping Address: Warehouse No. 7, MIDC, Chakan, Pune, Maharashtra - 410501
# GST No.: 27ABCDE1234F1Z5
# Contact Person: Mr. Rajesh Sharma
# Contact Number: +91 98765 43210
# Email: rajesh.sharma@abcindustries.com
# Material Details:
# Item Name	Quantity	Unit Price (INR)	Total Price (INR)
# Aluminum Wire Rods	500 kg	250/kg	1,25,000
# Copper Sheets	200 kg	700/kg	1,40,000
# Payment & Delivery Terms:
# Payment Terms: 50% advance, balance on delivery
# Mode of Payment: NEFT/RTGS
# Delivery Date: On or before February 15, 2025
# Delivery Mode: By road transport
# Kindly confirm the availability of the materials and share the proforma invoice at the earliest. Please process the order as per the agreed terms and dispatch it as soon as possible.

# Feel free to contact me for any clarifications.

# Looking forward to your confirmation.

# Best regards,
# Rajesh Sharma
# Purchase Manager
# ABC Industries Pvt. Ltd.
# +91 98765 43210
# rajesh.sharma@abcindustries.com"""

mail = st.text_input("Enter Email/Text Invoice")

submit = st.button("Extract")

if submit:
    response = parse_mail(mail)
    pprint(response)
    st.json(response, expanded=True)