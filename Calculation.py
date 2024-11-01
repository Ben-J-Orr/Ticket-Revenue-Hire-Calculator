import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
from fpdf import FPDF
import tempfile

def calculate_revenue(num_online_tickets: int, online_ticket_price: float, num_door_tickets: int, door_ticket_price: float, venue_hire_percent: float = 0.2):
    online_sales_revenue = num_online_tickets * online_ticket_price
    door_sales_revenue = num_door_tickets * door_ticket_price
    total_ticket_revenue = online_sales_revenue + door_sales_revenue
    total_ticket_hire = (num_online_tickets + num_door_tickets) * 2
    total_venue_hire = max((total_ticket_revenue - total_ticket_hire) * venue_hire_percent, 100)
    total_bacs_payment = total_ticket_hire + total_venue_hire
    return online_sales_revenue, door_sales_revenue, total_ticket_revenue, total_ticket_hire, total_venue_hire, total_bacs_payment

def generate_pdf(act_name, date_of_performance, door_person, sound_engineer, num_online_tickets, num_door_tickets, total_tickets_sold, online_sales_revenue, door_sales_revenue, total_ticket_revenue, total_ticket_hire, total_venue_hire, total_bacs_payment):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt="Gig Details & Calculated Costs", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, txt="Act Details", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Act Name: {act_name}", ln=True)
    pdf.cell(0, 10, txt=f"Date of Performance: {date_of_performance.strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(0, 10, txt=f"Door Person: {door_person}", ln=True)
    pdf.cell(0, 10, txt=f"Sound Engineer: {sound_engineer}", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, txt="Ticket Sales Breakdown", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Number of Online Tickets Sold: {num_online_tickets}", ln=True)
    pdf.cell(0, 10, txt=f"Number of Door Tickets Sold: {num_door_tickets}", ln=True)
    pdf.cell(0, 10, txt=f"Total Tickets Sold: {total_tickets_sold}", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, txt="Revenue Breakdown", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Total Online Ticket Revenue: £{online_sales_revenue:.2f}", ln=True)
    pdf.cell(0, 10, txt=f"Total Door Ticket Revenue: £{door_sales_revenue:.2f}", ln=True)
    pdf.cell(0, 10, txt=f"Total Sales (Both Online and Door): £{total_ticket_revenue:.2f}", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, txt="Hire and BACs Payment", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Total Ticket Hire: £{total_ticket_hire:.2f}", ln=True)
    pdf.cell(0, 10, txt=f"Total Venue Hire: £{total_venue_hire:.2f}", ln=True)
    pdf.cell(0, 10, txt=f"Total BACs Payment: £{total_bacs_payment:.2f}", ln=True)
    if total_venue_hire == 100:
        pdf.set_text_color(255, 0, 0)
        pdf.multi_cell(0, 10, txt="Note: The minimum venue hire of £100 has been applied because the calculated value was below this threshold.")
        pdf.set_text_color(0, 0, 0)

    return pdf

st.set_page_config(page_title="Ticket Revenue & Hire Calculator", layout="wide")

st.sidebar.header("Enter Gig Details")
act_name = st.sidebar.text_input("Act Name:")
date_of_performance = st.sidebar.date_input("Date of Performance:", min_value=date.today())
door_person = st.sidebar.text_input("Door Person:")
sound_engineer = st.sidebar.text_input("Sound Engineer:")
num_online_tickets = st.sidebar.number_input("Number of Online Tickets Sold:", min_value=0, value=0, step=1)
online_ticket_price = st.sidebar.number_input("Online Ticket Price (£):", min_value=0.0, value=10.0, step=0.5)
num_door_tickets = st.sidebar.number_input("Number of Door Tickets Sold:", min_value=0, value=0, step=1)
door_ticket_price = st.sidebar.number_input("Door Ticket Price (£):", min_value=0.0, value=10.0, step=0.5)
venue_hire_percent = st.sidebar.slider("Venue Hire Percentage (Default 20%):", min_value=0, max_value=100, value=20) / 100

if st.sidebar.button("Calculate Revenue"):
    if not act_name:
        st.sidebar.error("Please enter the Act Name.")
    elif not door_person:
        st.sidebar.error("Please enter the Door Person's name.")
    elif not sound_engineer:
        st.sidebar.error("Please enter the Sound Engineer's name.")
    elif num_online_tickets == 0 and num_door_tickets == 0:
        st.sidebar.error("Please enter the number of tickets sold (at least one).")
    else:
        online_sales_revenue, door_sales_revenue, total_ticket_revenue, total_ticket_hire, total_venue_hire, total_bacs_payment = calculate_revenue(
            num_online_tickets, online_ticket_price, num_door_tickets, door_ticket_price, venue_hire_percent
        )
        total_tickets_sold = num_online_tickets + num_door_tickets

        st.markdown('## Act Details')
        st.markdown(f'**Act Name:** `{act_name}`')
        st.markdown(f'**Date of Performance:** `{date_of_performance.strftime("%d/%m/%Y")}`')
        st.markdown(f'**Door Person:** `{door_person}`')
        st.markdown(f'**Sound Engineer:** `{sound_engineer}`')

        st.markdown("---")

        st.markdown('## Ticket Sales Breakdown')
        st.markdown(f'**Number of Online Tickets Sold:** `{num_online_tickets}`')
        st.markdown(f'**Number of Door Tickets Sold:** `{num_door_tickets}`')
        st.markdown(f'**Total Tickets Sold:** `{total_tickets_sold}`')

        st.markdown("---")

        st.markdown('## Revenue Breakdown')
        st.markdown(f'**Total Online Ticket Revenue:** `£{online_sales_revenue:.2f}`')
        st.markdown(f'**Total Door Ticket Revenue:** `£{door_sales_revenue:.2f}`')
        st.markdown(f'**Total Sales (Both Online and Door):** `£{total_ticket_revenue:.2f}`')

        st.markdown("---")

        st.markdown('## Hire and BACs Payment')
        st.markdown(f'**Total Ticket Hire:** `£{total_ticket_hire:.2f}`')
        st.markdown(f'**Total Venue Hire:** `£{total_venue_hire:.2f}`')
        st.markdown(f'**Total BACs Payment:** `£{total_bacs_payment:.2f}`')
        if total_venue_hire == 100:
            st.markdown(':orange[Note: The minimum venue hire of £100 has been applied because the calculated value was below this threshold.]')

        pdf = generate_pdf(act_name, date_of_performance, door_person, sound_engineer, num_online_tickets, num_door_tickets, total_tickets_sold, online_sales_revenue, door_sales_revenue, total_ticket_revenue, total_ticket_hire, total_venue_hire, total_bacs_payment)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(temp_file.name)

        with open(temp_file.name, "rb") as pdf_file:
            st.download_button(label="Download PDF", data=pdf_file.read(), file_name=f"{act_name}_{date_of_performance.strftime('%Y-%m-%d')}.pdf", mime="application/pdf")

# To run this code, save it in a Python (.py) file and run `streamlit run filename.py` in the terminal.
