import streamlit as st
import datetime

# Page Configuration
st.set_page_config(page_title="SBBT Quotation Generator", page_icon="🏗️", layout="wide")

# Custom CSS for Premium UI & Print Layout
st.markdown("""
<style>
    .report-container {
        background-color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #333333;
        padding: 30px;
        border: 2px solid #1B365D;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
    }
    .brand-title {
        color: #1B365D;
        font-size: 28px;
        font-weight: bold;
        margin: 0;
    }
    .brand-sub {
        color: #4A90E2;
        font-size: 14px;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 0;
    }
    .quote-badge {
        background-color: #1B365D;
        color: white;
        padding: 10px 20px;
        font-weight: bold;
        border-radius: 5px;
        text-align: center;
    }
    .section-title {
        background-color: #1B365D;
        color: white;
        padding: 8px 12px;
        font-size: 16px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
        border-radius: 3px;
    }
    .client-line {
        font-style: italic;
        color: #555555;
        background-color: #F4F7FA;
        padding: 15px;
        border-left: 4px solid #4A90E2;
        margin: 15px 0;
        font-size: 15px;
    }
    th {
        background-color: #F4F7FA;
        color: #1B365D;
        text-align: left;
        padding: 10px;
        border-bottom: 2px solid #D3D3D3;
    }
    td {
        padding: 10px;
        border-bottom: 1px solid #EAEAEA;
    }
    .total-row {
        font-weight: bold;
        background-color: #EAEAEA;
    }
    @media print {
        .no-print { display: none !important; }
        .report-container { border: none; box-shadow: none; padding: 0; }
    }
</style>
""", unsafe_allow_safe_html=True)

# 1. SIMPLE LOGIN SYSTEM (Expansion Ready)
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.subheader("🔑 SBBT Portal Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "sbbt_admin" and password == "sbbt@2026": # Secure passwords in secrets later
            st.session_state['authenticated'] = True
            st.rerun()
        else:
            st.error("Invalid Credentials")
    st.stop()

# 2. APP SIDEBAR INPUTS (Control Panel)
st.sidebar.header("🛠️ Quotation Configurator")

client_name = st.sidebar.text_input("Client Name", "Rahul Sharma")
project_address = st.sidebar.text_input("Project Address", "Sector 45, Gurgaon")
plot_area_yd = st.sidebar.number_input("Plot Area (Sq. Yards)", min_value=10, max_value=1000, value=150)
built_up_area = st.sidebar.number_input("Total Built-up Area (Sq. Ft.)", min_value=100, max_value=20000, value=3500)

floors_type = st.sidebar.selectbox("Floor Configuration", ["G+1/2", "G+3/4"])

package_type = st.sidebar.selectbox("Select Base Package", ["Core Shell Only", "Essential Package", "Premium Luxury"])

# Customizable Pricing Sliders based on package
if package_type == "Core Shell Only":
    psf_rate = st.sidebar.slider("Custom Rate (PSF)", 1199, 1248, 1199)
elif package_type == "Essential Package":
    psf_rate = st.sidebar.slider("Custom Rate (PSF)", 1699, 1848, 1699)
else:
    psf_rate = st.sidebar.slider("Custom Rate (PSF)", 2099, 2499, 2099)

# Addons Configuration
st.sidebar.subheader("➕ Optional Addons")
elevator_floors = st.sidebar.number_input("Elevator Provision (No. of Floors)", min_value=0, max_value=10, value=0)
elevator_units = st.sidebar.number_input("Full Elevator Installation (4 Pax Units)", min_value=0, max_value=5, value=0)

# Custom Client-Centric Line Generator (Dynamic Text box)
st.sidebar.subheader("✍️ Client Centric Touch")
custom_note = st.sidebar.text_area(
    "Custom Dedication Line", 
    f"Dear {client_name}, this bespoke blueprint is engineered to transform your vision at {project_address} into a structural masterpiece, blending uncompromising seismic safety with timeless architectural elegance."
)

# 3. CALCULATION LOGIC
# Timeline evaluation
timeline = "6 Months" if floors_type == "G+1/2" else "9 Months"

# Cost Calculations
base_construction_cost = built_up_area * psf_rate
elevator_provision_cost = elevator_floors * 30000
elevator_kit_cost = elevator_units * 850000
net_total = base_construction_cost + elevator_provision_cost + elevator_kit_cost

# 4. DESIGNER QUOTATION GENERATOR (HTML OUTPUT)
st.title("🏗️ SBBT Premium Quotation Engine")
st.caption("Configure inputs on the left sidebar. Press Ctrl+P to save the styled block as PDF.")

# Styled HTML Block
quote_html = f"""
<div class="report-container">
    <table class="header-table">
        <tr>
            <td>
                <div class="brand-title">SHREE BADREE BUILD TECH PVT LTD</div>
                <div class="brand-sub">Premium Residential Construction</div>
            </td>
            <td style="text-align: right; width: 30%;">
                <div class="quote-badge">QUOTATION</div>
                <p style="margin: 5px 0 0 0; font-size: 12px; color: #555555;">
                    <b>Date:</b> {datetime.date.today().strftime('%d %B %Y')}<br>
                    <b>Validity:</b> 30 Days
                </p>
            </td>
        </tr>
    </table>
    
    <hr style="border: 0; border-top: 1px solid #1B365D; margin-bottom: 20px;">
    
    <div class="client-line">
        "{custom_note}"
    </div>
    
    <table style="width:100%; margin-bottom: 20px; font-size: 14px;">
        <tr>
            <td><b>Prepared For:</b> {client_name}</td>
            <td><b>Plot Area:</b> {plot_area_yd} Sq. Yards</td>
        </tr>
        <tr>
            <td><b>Project Site:</b> {project_address}</td>
            <td><b>Built-up Area:</b> {built_up_area} Sq. Ft.</td>
        </tr>
        <tr>
            <td><b>Project Timeline:</b> {timeline} ({floors_type})</td>
            <td><b>Selected Tier:</b> {package_type} (@ ₹{psf_rate}/PSF)</td>
        </tr>
    </table>
    
    <div class="section-title">PROJECT COST ESTIMATE & COMPONENT BREAKDOWN</div>
    <table style="width:100%; border-collapse: collapse;">
        <thead>
            <tr>
                <th>Scope Description</th>
                <th style="text-align: right;">Rate / Metrics</th>
                <th style="text-align: right;">Amount (INR)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><b>Base Structural & Finishing Work</b><br><small>As per {package_type} specifications</small></td>
                <td style="text-align: right;">₹{psf_rate} / Sq.Ft.</td>
                <td style="text-align: right;">₹ {base_construction_cost:,.2f}</td>
            </tr>
"""

if elevator_floors > 0:
    quote_html += f"""
            <tr>
                <td><b>Elevator Shaft Provision</b><br><small>Civil & structural alignment</small></td>
                <td style="text-align: right;">{elevator_floors} Floors @ ₹30,000</td>
                <td style="text-align: right;">₹ {elevator_provision_cost:,.2f}</td>
            </tr>
    """

if elevator_units > 0:
    quote_html += f"""
            <tr>
                <td><b>Full Elevator Kit & Installation</b><br><small>4 Passenger premium setup</small></td>
                <td style="text-align: right;">{elevator_units} Unit(s) @ ₹8,50,000</td>
                <td style="text-align: right;">₹ {elevator_kit_cost:,.2f}</td>
            </tr>
    """

quote_html += f"""
            <tr class="total-row">
                <td>Estimated Net Total (Excluding GST)</td>
                <td></td>
                <td style="text-align: right;">₹ {net_total:,.2f}</td>
            </tr>
        </tbody>
    </table>
    
    <div class="section-title">PACKAGE SPECIFICATIONS & INCLUSIONS</div>
    <div style="font-size: 13px; line-height: 1.6; color: #444444; padding: 10px;">
"""

# Dynamic Inclusions/Exclusions Based on Selected Package
if package_type == "Core Shell Only":
    quote_html += """
        <ul>
            <li><b>Structure:</b> Complete RCC framework as per structural designs (M25 Ready-Mix Concrete).</li>
            <li><b>Steel & Masonry:</b> Rathi TMT Steel (or equivalent) with Premium AAC Blocks / Red Bricks.</li>
            <li><b>Electricals:</b> Concealed PVC Conduits laid in slabs & walls only (No wiring or switches included).</li>
            <li><span style="color:red;"><b>Major Exclusions:</b></span> Electrical wires, switches, plumbing lines, flooring, painting, doors, windows, and modular woodwork.</li>
        </ul>
    """
elif package_type == "Essential Package":
    quote_html += """
        <ul>
            <li><b>Plumbing & Tanks:</b> Astral/Prince CPVC & SWR pipes, basic Hindware/Jaquar sanitary setups, and 500L/1000L Sintex water tank per 1000 sq ft area.</li>
            <li><b>Electricals:</b> Havells / Polycab / Plaza / RR FRLS wire with basic modular switches & MCBs.</li>
            <li><b>Ceiling & Finish:</b> 1 Designer False Ceiling in Drawing Room only; Basic POP Cornice designs in other areas.</li>
            <li><b>Flooring & Stones:</b> Somany 2'x2' vitrified tiles (Budget upto ₹40/sq.ft.) and P. White Granite layout in parking zones.</li>
        </ul>
    """
else:
    quote_html += """
        <ul>
            <li><b>Premium Structural Setup:</b> Heavy-duty framework utilizing premium <b>Jindal / Tata TMT bars</b>.</li>
            <li><b>Luxury Plumbing:</b> Wall-Hung Jaquar (or similar) fixtures, integrated Diverter Lines, and high-efficiency Output Pressure Motors with 1000L Sintex tanks.</li>
            <li><b>Full Interior Woodwork:</b> Standard Modular Kitchen (8'x5') + Wardrobes (4'x9') in every bedroom featuring branded boards/fittings with a <b>5-Year Company Warranty</b>.</li>
            <li><b>Premium Finishes:</b> Designer False Ceiling in every room, premium 2'x4' Somany/Johnson/Nitco tiles, Anti-skid roof tiles, and SS304 main gates/staircase glass railings.</li>
            <li><b>Smart Tech:</b> Integrated 6-Channel CCTV surveillance network and Smart Electronic Digital Gate Lock.</li>
        </ul>
    """

quote_html += """
    </div>
    
    <div style="margin-top: 30px; font-size: 11px; color: #777777; text-align: center;">
        Building Trust Through Quality & Transparency • Shree Badree Build Tech Pvt Ltd
    </div>
</div>
"""

# Render HTML in Streamlit
st.markdown(quote_html, unsafe_allow_safe_html=True)
