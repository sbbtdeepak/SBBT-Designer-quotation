import streamlit as st
import pandas as pd
import datetime

# 1. PAGE LAYOUT CONFIGURATION
st.set_page_config(page_title="SBBT Premium Quotation Engine", page_icon="🏗️", layout="centered")

# 2. ADMIN GATEWAY SYSTEM
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("🏗️ SBBT Enterprise Portal")
    st.write("Shree Badree Build Tech Pvt. Ltd. — Administrative Login")
    
    with st.form("Access Portal"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_submitted = st.form_submit_button("Authenticate Entry")
        
        if login_submitted:
            if username == "sbbt_admin" and password == "sbbt@2026":
                st.session_state['authenticated'] = True
                st.success("Authorized! Loading Engine...")
                st.rerun()
            else:
                st.error("Access Denied: Invalid Administrative Credentials")
    st.stop()

# 3. EXECUTIVE CONTROL PANEL
st.title("🎛️ SBBT Premium Estimation Panel")
st.write("---")

# Section 1: Client Profile Matrix
st.subheader("👤 Client & Site Profile")
c_col1, c_col2 = st.columns(2)
with c_col1:
    client_name = st.text_input("Client Name", "Mr. & Mrs. Sharma")
    project_address = st.text_input("Site Location/Address", "Palam, Gurgaon (HR)")
with c_col2:
    plot_area_yd = st.number_input("Plot Area (Sq. Yards)", min_value=10, max_value=2000, value=150)
    total_floors = st.slider("Number of Floors to Build (including Stilt/Ground)", min_value=1, max_value=6, value=3)

# AUTOMATIC CORE CALCULATION (1 Sq.Yard = 9 Sq.Feet)
plot_area_ft = plot_area_yd * 9

st.write("---")

# Section 2: Floor-Wise Detail Matrix Configuration
st.subheader("📐 Architectural Floor Breakout & Rates")
st.caption(f"Note: Based on your Plot Area, each floor is automatically set to **{plot_area_ft} Sq.Ft.**")

floor_data = []
default_packages = ["Solid Structure Core (₹1199)", "Essential Finishing (₹1699)", "Premium Luxury Profile (₹2099)"]

# Generating inputs dynamically for each floor using the master Plot Area
for i in range(total_floors):
    if i == 0:
        floor_label = "Ground Floor / Stilt"
    elif i == 1:
        floor_label = "First Floor"
    elif i == 2:
        floor_label = "Second Floor"
    elif i == 3:
        floor_label = "Third Floor"
    else:
        floor_label = f"{i}th Floor"
        
    st.write(f"**🏗️ Rate Settings for {floor_label}**")
    f_col1, f_col2 = st.columns(2)
    
    with f_col1:
        f_pack = st.selectbox(f"Package Profile", default_packages, index=2, key=f"pack_{i}")
    with f_col2:
        if "Solid Structure" in f_pack:
            min_p, max_p, def_p = 1100, 1500, 1199
        elif "Essential" in f_pack:
            min_p, max_p, def_p = 1500, 2000, 1699
        else:
            min_p, max_p, def_p = 2000, 3000, 2399
            
        f_rate = st.number_input(f"Custom Rate (₹/PSF)", min_value=min_p, max_value=max_p, value=def_p, key=f"rate_{i}")
    
    floor_data.append({
        "Floor Profile": floor_label, 
        "Package Profile": f_pack.split(" (")[0], 
        "Area (Sq.Ft)": plot_area_ft, 
        "Rate (₹/PSF)": f_rate
    })

st.write("---")

# Section 3: Notes & Personalization
st.subheader("✍️ Executive Customization & Strategy Notes")
custom_note = st.text_area(
    "Custom Dedication Line (Client-Centric Touch)", 
    f"We are offering a special commercial advantage for your property at {project_address} while maintaining premium specifications and long-term value, ensuring trust with zero compromises."
)
additional_reqs = st.text_area("Additional Requirements / Custom Structural Commitments", "Includes 15+ luxury upgrades, earthquake resistant RCC frame configuration, and a comprehensive 2-Year AMC covering operational support.")

# 4. MATHEMATICAL COMPUTATION
total_built_up = plot_area_ft * total_floors
net_project_cost = sum(item['Area (Sq.Ft)'] * item['Rate (₹/PSF)'] for item in floor_data)

# Convert data to clean DataFrame for elegant display
df_breakout = pd.DataFrame(floor_data)
df_breakout["Subtotal Amount (INR)"] = df_breakout["Area (Sq.Ft)"] * df_breakout["Rate (₹/PSF)"]
df_breakout["Subtotal Amount (INR)"] = df_breakout["Subtotal Amount (INR)"].map("₹ {:,.2f}".format)

# 5. ELEGANT EXECUTIVE PROPOSAL DISPLAY (100% Crash-Proof Native)
st.write("---")
st.write("### 📈 SBBT Official Commercial Proposal")
st.caption("💡 Tip: Click on the preview block below and press **Ctrl + P** to save or print this proposal cleanly.")

with st.container(border=True):
    # Corporate Identity Header
    st.subheader("SHREE BADREE BUILD TECH PVT. LTD.")
    st.caption("WHERE VISION MEETS PRECISION • TRUSTED SINCE 2011")
    st.write(f"**Google Rating:** 4.9/5.0 (50+ Happy Families)")
    st.write("---")
    
    # Meta Details columns
    m1, m2 = st.columns(2)
    with m1:
        st.write(f"**Quotation Ref:** SBBT/Q/{datetime.date.today().year}/092")
        st.write(f"**Client Name:** {client_name}")
        st.write(f"**Project Site Location:** {project_address}")
    with m2:
        st.write(f"**Date Issued:** {datetime.date.today().strftime('%d %B %Y')}")
        st.write(f"**Plot Size:** {plot_area_yd} Sq. Yards ({plot_area_ft} Sq. Ft.)")
        st.write(f"**Total Built-up Area:** {total_built_up:,} Sq. Ft. ({total_floors} Floors)")
        
    st.write("---")
    
    # Executive Narrative Box
    st.info(f"\"{custom_note}\"")
    st.write("")
    
    st.write("**📋 DETAILED ARCHITECTURAL COST BREAKOUT:**")
    # Rendering clean structured table using native safe dataframe component
    st.dataframe(df_breakout, hide_index=True, use_container_width=True)
        
    st.write("")
    # Premium Big Text display using standard Streamlit Metric layout
    st.metric(label="TOTAL ESTIMATED CONSTRUCTION COST (Excl. GST)", value=f"₹ {net_project_cost:,.2f}")
    st.write("---")
    
    # Inclusions Matrix
    st.write("**⚙️ STRUCTURAL EXTRA ADVANTAGES & COMMITMENTS:**")
    st.warning(additional_reqs)
    
    st.write("**🛡️ CORE STANDARD INCLUSIONS ACROSS ALL SCOPES:**")
    st.markdown("""
    * **Heavy Duty Structural Core:** Complete RCC framework designed for highest seismic safety standards using RMC M25 Concrete and premium Rathi Fe500 steel layout.
    * **High-Grade Masonry:** Premium internal & external block work built with durable AAC Blocks or classic Red Bricks wrapped in rich cement mortar plaster.
    * **Quality Governance:** End-to-end transparent processing with detailed material checklists, continuous site monitoring, and formal project tracking.
    """)
    
    st.write("---")
    
    # Signature Grid
    f1, f2 = st.columns(2)
    with f1:
        st.write("")
        st.caption("Authorized Signatory")
        st.write("**Shree Badree Build Tech Pvt. Ltd.**")
    with f2:
        st.write("📞 **Contact:** +91 8800614403, 9625803339")
        st.write("📧 **Email:** deeep1sharma@gmail.com")
        st.caption("Building Trust Through Quality & Transparency")
