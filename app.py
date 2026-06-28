import streamlit as st
import datetime

# 1. PAGE LAYOUT CONFIGURATION
st.set_page_config(page_title="SBBT Premium Quotation Engine", page_icon="🏗️", layout="centered")

# 2. ADMIN GATEWAY SYSTEM (Zero HTML Dependency)
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
    total_floors = st.slider("Number of Floors to Build", min_value=1, max_value=6, value=3)

st.write("---")

# Section 2: Floor-Wise Detail Matrix Configuration
st.subheader("📐 Architectural Floor Breakout & Rates")

floor_data = []
default_packages = ["Solid Structure Core", "Essential Finishing", "Premium Luxury Profile"]

# Generating inputs dynamically for each floor
for i in range(total_floors):
    floor_label = f"Ground Floor" if i == 0 else f"First Floor" if i == 1 else f"Second Floor" if i == 2 else f"Third Floor" if i == 3 else f"Floor {i}"
    
    st.write(f"**🏗️ Configuration for {floor_label}**")
    f_col1, f_col2, f_col3 = st.columns(3)
    
    with f_col1:
        f_area = f_area = st.number_input(f"Area (Sq.Ft)", min_value=50, max_value=5000, value=1800, key=f"area_{i}")
    with f_col2:
        f_pack = st.selectbox(f"Package Profile", default_packages, index=2, key=f"pack_{i}")
    with f_col3:
        if f_pack == "Solid Structure Core":
            min_p, max_p, def_p = 1100, 1500, 1199
        elif f_pack == "Essential Finishing":
            min_p, max_p, def_p = 1500, 2000, 1699
        else:
            min_p, max_p, def_p = 2000, 3000, 2399
            
        f_rate = st.number_input(f"Custom Rate (₹/PSF)", min_value=min_p, max_value=max_p, value=def_p, key=f"rate_{i}")
    
    floor_data.append({"floor": floor_label, "area": f_area, "package": f_pack, "rate": f_rate})

st.write("---")

# Section 3: Notes & Personalization
st.subheader("✍️ Executive Customization & Strategy Notes")
custom_note = st.text_area(
    "Custom Dedication Line (Client-Centric Touch)", 
    f"We are offering a special commercial advantage for your property at {project_address} while maintaining premium specifications and long-term value, ensuring trust with zero compromises."
)
additional_reqs = st.text_area("Additional Requirements / Custom Structural Commitments", "Includes 15+ luxury upgrades, earthquake resistant RCC frame configuration, and a comprehensive 2-Year AMC covering operational support.")

# 4. MATHEMATICAL COMPUTATION
total_built_up = sum(item['area'] for item in floor_data)
net_project_cost = sum(item['area'] * item['rate'] for item in floor_data)

# 5. ELEGANT EXECUTIVE PROPOSAL DISPLAY (100% Native Containers)
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
        st.write(f"**Plot Dimensions:** {plot_area_yd} Sq. Yards")
        st.write(f"**Total Built-up Area:** {total_built_up:,} Sq. Ft.")
        
    st.write("---")
    
    # Executive Narrative Box
    st.info(f"\"{custom_note}\"")
    st.write("")
    
    st.write("**📋 ITEMIZED ARCHITECTURAL COST BREAKDOWN:**")
    st.write("")
    
    # Rendering Floor Items using dynamic layouts without raw HTML tables
    for item in floor_data:
        f_cost = item['area'] * item['rate']
        st.write(f"**{item['floor']}** — *{item['package']}*")
        st.write(f"↳ Metrics: {item['area']:,} Sq.Ft. @ ₹{item['rate']:,}/PSF")
        st.write(f"**Subtotal Amount:** ₹ {f_cost:,.2f}")
        st.write("-" * 30)
        
    st.write("")
    # Premium Big Text display using standard Streamlit Metric layout
    st.metric(label="TOTAL ESTIMATED CONSTRUCTION COST (Excl. GST)", value=f"₹ {net_project_cost:,.2f}")
    st.write("---")
    
    # Inclusions Matrix
    st.write("**⚙️ STRUCTURAL EXTRA ADVANTAGES & COMMITMENTS:**")
    st.warning(additional_reqs)
    
    st.write("**🛡️ CORE STANDARD INCLUSIONS ACROSS ALL SCOPES:**")
    st.markdown("""
    * **Heavy Duty Structural Core:** Complete RCC framework designed for highest seismic safety standards using RMC M25 Concrete and premium Rathi Fe500 steel layout[cite: 293, 295, 297, 306].
    * **High-Grade Masonry:** Premium internal & external block work built with durable AAC Blocks or classic Red Bricks wrapped in rich cement mortar plaster[cite: 298, 299].
    * **Quality Governance:** End-to-end transparent processing with detailed material checklists, continuous site monitoring, and formal project tracking[cite: 324, 325, 326].
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
