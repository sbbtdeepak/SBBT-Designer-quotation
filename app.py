import streamlit as st
import datetime

# Page Configuration
st.set_page_config(page_title="SBBT Quotation Generator", page_icon="🏗️", layout="wide")

# SOLUTION: HTML/CSS Static Block standard markdown string mein (f-string hatadi hai)
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
    .report-container th {
        background-color: #F4F7FA;
        color: #1B365D;
        text-align: left;
        padding: 10px;
        border-bottom: 2px solid #D3D3D3;
    }
    .report-container td {
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

# 1. AUTHENTICATION SYSTEM
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.subheader("🔑 SBBT Portal Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "sbbt_admin" and password == "sbbt@2026":
            st.session_state['authenticated'] = True
            st.sidebar.success("Logged In Successfully!")
            st.rerun()
        else:
            st.error("Invalid Credentials")
    st.stop()

# 2. CONTROL PANEL INPUTS
st.sidebar.header("🛠️ Quotation Configurator")

client_name = st.sidebar.text_input("Client Name", "Rahul Sharma")
project_address = st.sidebar.text_input("Project Address", "Sector 45, Gurgaon")
plot_area_yd = st.sidebar.number_input("Plot Area (Sq. Yards)", min_value=10, max_value=1000, value=150)
built_up_area = st.sidebar.number_input("Total Built-up Area (Sq. Ft.)", min_value=100, max_value=20000, value=3500)
floors_type = st.sidebar.selectbox("Floor Configuration", ["G+1/2", "G+3/4"])
package_type = st.sidebar.selectbox("Select Base Package", ["Core Shell Only", "Essential Package", "Premium Luxury"])

# Price constraints management
if package_type == "Core Shell Only":
    psf_rate = st.sidebar.slider("Custom Rate (PSF)", 1199, 1248, 1199)
elif package_type == "Essential Package":
    psf_rate = st.sidebar.slider("Custom Rate (PSF)", 1699, 1848, 1699)
else:
    psf_rate = st.sidebar.slider("Custom Rate (PSF)", 2099, 2499, 2099)

st.sidebar.subheader("➕ Optional Addons")
elevator_floors = st.sidebar.number_input("Elevator Provision (No. of Floors)", min_value=0, max_value=10, value=0)
elevator_units = st.sidebar.number_input("Full Elevator Installation (4 Pax Units)", min_value=0, max_value=5, value=0)

st.sidebar.subheader("✍️ Client Centric Touch")
custom_note = st.sidebar.text_area(
    "Custom Dedication Line", 
    f"Dear {client_name}, this bespoke blueprint is engineered to transform your vision at {project_address} into a structural masterpiece, blending uncompromising seismic safety with timeless architectural elegance."
)

# 3. METRIC EVALUATIONS
timeline = "6 Months" if floors_type == "G+1/2" else "9 Months"
base_cost = built_up_area * psf_rate
ele_prov_cost = elevator_floors * 30000
ele_kit_cost = elevator_units * 850000
net_total = base_cost + ele_prov_cost + ele_kit_cost

# 4. STRUCTURED HTML GENERATION (Safe implementation without bracket mixing)
st.title("🏗️ SBBT Premium Quotation Engine")
st.caption("Configure inputs on the left sidebar. Press Ctrl+P to save the styled block as PDF.")

# Header Component
st.markdown(f"""
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
    <div class="client-line">"{custom_note}"</div>
    <table style="width:100%; margin-bottom: 20px; font-size: 14px;">
        <tr><td><b>Prepared For:</b> {client_name}</td><td><b>Plot Area:</b> {plot_area_yd} Sq. Yards</td></tr>
        <tr><td><b>Project Site:</b> {project_address}</td><td><b>Built-up Area:</b> {built_up_area} Sq. Ft.</td></tr>
        <tr><td><b>Project Timeline:</b> {timeline} ({floors_type})</td><td><b>Selected Tier:</b> {package_type} (@ ₹{psf_rate}/PSF)</td></tr>
    </table>
    <div class="section-title">PROJECT COST ESTIMATE & COMPONENT BREAKDOWN</div>
    <table style="width:100%; border-collapse: collapse;">
        <thead>
            <tr><th>Scope Description</th><th style="text-align: right;">Rate / Metrics</th><th style="text-align: right;">Amount (INR)</th></tr>
        </thead>
        <tbody>
            <tr>
                <td><b>Base Structural & Finishing Work</b><br><small>As per {package_type} specifications</small></td>
                <td style="text-align: right;">₹{psf_rate} / Sq.Ft.</td>
                <td style="text-align: right;">₹ {base_cost:,.2f}</td>
            </tr>
""", unsafe_allow_safe_html=True)

# Conditional Components
if elevator_floors > 0:
    st.markdown(f"""
            <tr>
                <td><b>Elevator Shaft Provision</b><br><small>Civil & structural alignment</small></td>
                <td style="text-align: right;">{elevator_floors} Floors @ ₹30,000</td>
                <td style="text-align: right;">₹ {ele_prov_cost:,.2f}</td>
            </tr>
    """, unsafe_allow_safe_html=True)

if elevator_units > 0:
    st.markdown(f"""
            <tr>
                <td><b>Full Elevator Kit & Installation</b><br><small>4 Passenger premium setup</small></td>
                <td style="text-align: right;">{elevator_units} Unit(s) @ ₹8,50,000</td>
                <td style="text-align: right;">₹ {ele_kit_cost:,.2f}</td>
            </tr>
    """, unsafe_allow_safe_html=True)

# Total Footer & Inclusions
st.markdown(f"""
            <tr class="total-row">
                <td>Estimated Net Total (Excluding GST)</td>
                <td></td>
                <td style="text-align: right;">₹ {net_total:,.2f}</td>
            </tr>
        </tbody>
    </table>
    <div class="section-title">PACKAGE SPECIFICATIONS & INCLUSIONS</div>
    <div style="font-size: 13px; line-height: 1.6; color: #444444; padding: 10px;">
""", unsafe_allow_safe_html=True)

if package_type == "Core Shell Only":
    st.markdown("""
        <ul>
            <li><b>Structure:</b> Complete RCC framework as per structural drawings: Foundation, Columns, Beams, and Slabs using RMC M25 Concrete.</li>
            <li><b>Steel & Masonry:</b> Premium Rathi TMT Steel (or equivalent) with high-strength AAC Blocks or Red Bricks.</li>
            <li><b>Electricals:</b> Concealed PVC conduits laid inside slabs & walls only (Conduit only - no wiring, no switches).</li>
            <li><span style="color:red;"><b>Major Exclusions:</b></span> Finishing items, wiring, plumbing lines, flooring, and woodwork are excluded.</li>
        </ul>
    """, unsafe_allow_safe_html=True)
elif package_type == "Essential Package":
    st.markdown("""
        <ul>
            <li><b>Plumbing & Tanks:</b> Astral/Prince CPVC & SWR pipeline layout with standard Hindware/Jaquar basic CP fittings & English WC.</li>
            <li><b>Electricals:</b> Certified Havells / Polycab / Plaza / RR FRLS wire installations with standard modular switches & distribution board MCBs.</li>
            <li><b>Flooring & Accents:</b> Premium P. White Granite layout in parking, Black Granite stairs, and Somany 2'x2' vitrified floor tiles.</li>
            <li><b>Ceiling & Paint:</b> 1 Designer False Ceiling in Drawing Room only; Basic POP Cornice molding in all other rooms.</li>
        </ul>
    """, unsafe_allow_safe_html=True)
else:
    st.markdown("""
        <ul>
            <li><b>Structure & Steel:</b> Premium structural layout upgrading options up to heavy Tata/Jindal TMT bar distributions.</li>
            <li><b>Luxury Fittings:</b> Wall-Hung Jaquar setups, dedicated Diverter lines, output pressure motor distribution, and 1000L Sintex tanks per 1000 sq.ft.</li>
            <li><b>Modular Woodwork:</b> Complete Standard Modular Kitchen (8'x5') and high-grade board wardrobes (4'x9') in every bedroom with a 5-Year Company Warranty.</li>
            <li><b>Ceiling & Tech:</b> Full Designer Gypsum/POP False Ceiling in every single room, 6-Channel CCTV setup, and Smart Digital Gate Lock for advanced safety.</li>
        </ul>
    """, unsafe_allow_safe_html=True)

st.markdown("""
    </div>
    <div style="margin-top: 30px; font-size: 11px; color: #777777; text-align: center;">
        Building Trust Through Quality & Transparency • Shree Badree Build Tech Pvt Ltd
    </div>
</div>
""", unsafe_allow_safe_html=True)
