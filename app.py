import streamlit as st
import datetime

# Page Configuration
st.set_page_config(page_title="SBBT Quotation Portal", page_icon="🏗️", layout="centered")

# 1. LOGIN SYSTEM (Secure UI Gateway)
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("🏗️ SBBT Premium Portal")
    st.write("Welcome to Shree Badree Build Tech Pvt Ltd Dashboard.")
    
    with st.form("Login System"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_btn = st.form_submit_button("Secure Login")
        
        if submit_btn:
            if username == "sbbt_admin" and password == "sbbt@2026":
                st.session_state['authenticated'] = True
                st.success("Access Granted! Loading Engine...")
                st.rerun()
            else:
                st.error("Invalid Administrative Credentials")
    st.stop()

# 2. APPLICATION CORE CONTROL PANEL
st.title("📋 SBBT Premium Quotation Engine")
st.write("---")

# User Parameter Inputs divided in sections
st.subheader("🛠️ Step 1: Project Parameters")
col1, col2 = st.columns(2)

with col1:
    client_name = st.text_input("Client Name", "Rahul Sharma")
    project_address = st.text_input("Project Address", "Sector 45, Gurgaon")
    plot_area_yd = st.number_input("Plot Area (Sq. Yards)", min_value=10, max_value=1000, value=150)

with col2:
    built_up_area = st.number_input("Total Built-up Area (Sq. Ft.)", min_value=100, max_value=20000, value=3500)
    floors_type = st.selectbox("Floor Configuration Tiers", ["G+1/2", "G+3/4"])
    package_type = st.selectbox("Select Base Package Profile", ["Core Shell Only", "Essential Package", "Premium Luxury"])

# Contextual Sliders based on selected package profiles
st.subheader("💰 Step 2: Rate Customization")
if package_type == "Core Shell Only":
    psf_rate = st.slider("Custom Target Rate (PSF)", 1199, 1248, 1199)
elif package_type == "Essential Package":
    psf_rate = st.slider("Custom Target Rate (PSF)", 1699, 1848, 1699)
else:
    psf_rate = st.slider("Custom Target Rate (PSF)", 2099, 2499, 2099)

# Addon Cost Modifiers
st.subheader("➕ Step 3: Optional Infrastructure Addons")
col3, col4 = st.columns(2)
with col3:
    elevator_floors = st.number_input("Elevator Provision (No. of Floors)", min_value=0, max_value=10, value=0)
with col4:
    elevator_units = st.number_input("Full 4-Passenger Elevator Installation (Units)", min_value=0, max_value=5, value=0)

# Client Centric Narrative Section
st.subheader("✍️ Step 4: Client Centric Message personalization")
custom_note = st.text_area(
    "Quotation Header Dedication Line", 
    f"Dear {client_name}, this bespoke blueprint is engineered to transform your vision at {project_address} into a structural masterpiece, blending uncompromising seismic safety with timeless architectural elegance."
)

# 3. COMPUTATION INFRASTRUCTURE
timeline = "6 Months" if floors_type == "G+1/2" else "9 Months"
base_cost = built_up_area * psf_rate
ele_prov_cost = elevator_floors * 30000
ele_kit_cost = elevator_units * 850000
net_total = base_cost + ele_prov_cost + ele_kit_cost

# 4. STRUCTURED PREVIEW GENERATOR
st.write("---")
st.subheader("🖨️ Generated Executive Quotation View")

# Beautiful Box Outline using Native Components
with st.container(border=True):
    st.subheader("SHREE BADREE BUILD TECH PVT LTD")
    st.write("**PREMIUM RESIDENTIAL CONSTRUCTION SERVICES**")
    st.write(f"**Date:** {datetime.date.today().strftime('%d %B %Y')} | **Validity:** 30 Days")
    st.write("---")
    
    # Custom note block
    st.info(f"\"{custom_note}\"")
    st.write("")
    
    # Meta layout matrix
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.write(f"**Prepared For:** {client_name}")
        st.write(f"**Project Site:** {project_address}")
        st.write(f"**Project Timeline Framework:** {timeline} ({floors_type})")
    with m_col2:
        st.write(f"**Plot Area:** {plot_area_yd} Sq. Yards")
        st.write(f"**Total Area:** {built_up_area} Sq. Ft.")
        st.write(f"**Selected Tier Package:** {package_type} (@ ₹{psf_rate}/PSF)")
        
    st.write("---")
    st.write("**FINANCIAL ESTIMATE BREAKDOWN (INR):**")
    
    # Financial Rows
    st.write(f"* **Base Structural & Architectural Works:** ₹ {base_cost:,.2f}")
    if elevator_floors > 0:
        st.write(f"* **Elevator Civil Shaft Provision ({elevator_floors} Floors):** ₹ {ele_prov_cost:,.2f}")
    if elevator_units > 0:
        st.write(f"* **Full 4-Passenger Elevator System Setup ({elevator_units} Unit):** ₹ {ele_kit_cost:,.2f}")
        
    st.write("---")
    st.write(f"### **Estimated Net Project Cost (Excl. GST):** ₹ {net_total:,.2f}")
    st.write("---")
    
    # Inclusions Matrix
    st.write("**INCLUDED TECHNICAL TECHNICAL SPECIFICATIONS:**")
    if package_type == "Core Shell Only":
        st.markdown("""
        - **Structure Core:** Complete RCC framework as per designs (Foundation, Columns, Beams, Slabs using RMC M25 Concrete).
        - **Steel Distribution:** Premium Rathi TMT Steel layout configuration as per drawings.
        - **Masonry Elements:** High-Strength AAC Blocks / Red Bricks with cement mortar plastering.
        - **Conduiting System:** Concealed PVC conduits laid in slab & walls (Only conduits - no wires, no switches).
        - **Exclusions:** Plumbing, wiring, paint, flooring, finishes, doors, and windows are completely excluded.
        """)
    elif package_type == "Essential Package":
        st.markdown("""
        - **Plumbing Lines:** Astral/Prince CPVC & SWR layouts with basic Hindware/Jaquar sanitary setups & brass taps.
        - **Electrical Networks:** Certified Havells / Polycab / Plaza / RR FRLS wire sets with basic modular switches & MCBs.
        - **Flooring Matrix:** Somany 2'x2' vitrified tiles along with P. White Granite allocation in parking zones.
        - **Ceiling Finishes:** 1 Designer False Ceiling in Drawing Room; Rest areas wrapped with basic POP Cornice moldings.
        """)
    else:
        st.markdown("""
        - **Heavy Duty Framing:** Premium Structural Designs utilizing premium structural steel configurations.
        - **Luxury Outfitting:** Wall-Hung Jaquar configurations, specialized Diverter lines, and premium Output Pressure pumps.
        - **Internal Architecture:** Full Modular Kitchen (8'x5') + Wardrobes (4'x9') in every single bedroom with a 5-Year Corporate Warranty.
        - **Ceiling & Safety:** Full Designer POP/Gypsum false ceiling inside all rooms, 6-Channel CCTV setup, and Smart Digital Gate Lock.
        """)

    st.write("")
    st.center_text = st.write(" *Building Trust Through Quality & Transparency • SBBT Pvt Ltd* ")
