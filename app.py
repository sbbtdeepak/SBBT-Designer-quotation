import streamlit as st
import datetime

# Page configuration for a clean layout
st.set_page_config(page_title="SBBT Premium Quotation Engine", page_icon="🏗️", layout="centered")

# Custom UI Accent styling via native safe containers
st.markdown("""
    <style>
    div[data-testid="stForm"] {
        border: 2px solid #1B365D !important;
        background-color: #FAFAFA;
        border-radius: 8px;
    }
    div[data-testid="stMetricValue"] {
        color: #1B365D !important;
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
""", unsafe_allow_safe_html=True)

# 1. ADMIN GATEWAY SYSTEM
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("🏗️ SBBT Enterprise Portal")
    st.write("Shree Badree Build Tech Pvt. Ltd. — Administrative Login [cite: 1, 184]")
    
    with st.form("Access Portal"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_submitted = st.form_submit_button("Authenticate Entry")
        
        if login_submitted:
            if username == "sbbt_admin" and password == "sbbt@2026":
                st.session_state['authenticated'] = True
                st.success("Authorized! Directing to Core Quotation Engine...")
                st.rerun()
            else:
                st.error("Access Denied: Invalid Administrative Credentials")
    st.stop()

# 2. EXECUTIVE CONTROL PANEL
st.title("🎛️ SBBT Premium Estimation Panel")
st.write("Configure architectural parameters below to deploy a beautifully structured commercial proposal.")
st.write("---")

# Section 1: Client Metadata
st.subheader("👤 Client & Site Profile")
c_col1, c_col2 = st.columns(2)
with c_col1:
    client_name = st.text_input("Client Name", "Mr. & Mrs. Sharma") [cite: 5, 119, 198]
    project_address = st.text_input("Site Location/Address", "Palam, Gurgaon (HR)") [cite: 6, 120, 199, 201]
with c_col2:
    plot_area_yd = st.number_input("Plot Area (Sq. Yards)", min_value=10, max_value=2000, value=150)
    total_floors = st.slider("Number of Floors to Build", min_value=1, max_value=6, value=3)

st.write("---")

# Section 2: Floor-Wise Detail Matrix Configuration
st.subheader("📐 Architectural Floor Breakout & Rates")
st.write("Specify individual area metrics and customizable price limits as requested.")

floor_data = []
default_packages = ["Solid Structure Core", "Essential Finishing", "Premium Luxury Profile"] [cite: 8, 61, 125]

# Dynamic inputs block based on the number of floors selected
for i in range(total_floors):
    floor_label = f"Ground Floor" if i == 0 else f"Floor {i}" if i == 1 else f"Floor {i}"
    if i == 1: floor_label = "First Floor"
    if i == 2: floor_label = "Second Floor"
    if i == 3: floor_label = "Third Floor"
    
    st.markdown(f"**🏗️ Config for {floor_label}**")
    f_col1, f_col2, f_col3 = st.columns(3)
    
    with f_col1:
        f_area = f_area = st.number_input(f"Area (Sq.Ft) - {floor_label}", min_value=50, max_value=5000, value=1800, key=f"area_{i}") [cite: 207, 254]
    with f_col2:
        f_pack = st.selectbox(f"Package Standard - {floor_label}", default_packages, index=2, key=f"pack_{i}") [cite: 8, 61, 125]
    with f_col3:
        # Flexible base boundary metrics matching the master guidelines
        if f_pack == "Solid Structure Core":
            min_p, max_p, def_p = 1100, 1500, 1199 [cite: 9]
        elif f_pack == "Essential Finishing":
            min_p, max_p, def_p = 1500, 2000, 1699 [cite: 62]
        else:
            min_p, max_p, def_p = 2000, 3000, 2399 [cite: 123, 203, 254]
            
        f_rate = st.number_input(f"Custom Rate (₹/PSF) - {floor_label}", min_value=min_p, max_value=max_p, value=def_p, key=f"rate_{i}") [cite: 9, 62, 123, 203, 254]
    
    floor_data.append({"floor": floor_label, "area": f_area, "package": f_pack, "rate": f_rate})

st.write("---")

# Section 3: Addons & Narrative Personalization
st.subheader("✍️ Executive Customization & Strategy Notes")
custom_note = st.text_area(
    "Custom Dedication Line (Client-Centric Touch)", 
    f"We are offering a special commercial advantage for your property at {project_address} while maintaining premium specifications and long-term value, ensuring trust with zero compromises." [cite: 190, 191, 199, 269]
)
additional_reqs = st.text_area("Additional Requirements / Custom Structural Commitments", "Includes 15+ luxury upgrades, earthquake resistant RCC frame configuration, and a comprehensive 2-Year AMC covering operational support.") [cite: 164, 216, 230, 257]

# 3. HIGH-PRECISION VALUE ENGINE
total_built_up = sum(item['area'] for item in floor_data) [cite: 207, 254]
net_project_cost = sum(item['area'] * item['rate'] for item in floor_data) [cite: 254]

# 4. ELEGANT EXCLUSIVE PROPOSAL GENERATION VIEW
st.write("---")
st.subheader("📈 Previewing SBBT Corporate Quotation Layout")
st.info("💡 To save or print this clean elegant sheet instantly: Just click anywhere inside the preview container below and press **Ctrl + P** (or Cmd + P) to generate a premium print layout.")

# Elegant Document Wrapper Box
with st.container(border=True):
    # Corporate Identity Letterhead Header
    st.markdown("<h2 style='text-align: center; color: #1B365D; margin-bottom: 2px;'>SHREE BADREE BUILD TECH PVT. LTD.</h2>", unsafe_allow_safe_html=True) [cite: 184]
    st.markdown("<p style='text-align: center; font-size:12px; letter-spacing: 2px; color: #4A90E2; margin-top: 0px;'><b>WHERE VISION MEETS PRECISION</b></p>", unsafe_allow_safe_html=True) [cite: 185]
    st.markdown("<p style='text-align: center; font-size:11px; color:#555;'>Google Rating: <b>4.9/5.0</b> (50+ Happy Families) | Trusted Since 2011</p>", unsafe_allow_safe_html=True) [cite: 188, 189, 193]
    st.write("---")
    
    # Document Metadata Block
    m1, m2 = st.columns(2)
    with m1:
        st.write(f"**Quotation Ref:** SBBT/Q/{datetime.date.today().year}/092") [cite: 3, 117, 196]
        st.write(f"**Client Name:** {client_name}") [cite: 5, 119, 198]
        st.write(f"**Project Site:** {project_address}") [cite: 6, 120, 199, 201]
    with m2:
        st.write(f"**Date Issued:** {datetime.date.today().strftime('%d %B %Y')}") [cite: 4, 118, 197]
        st.write(f"**Plot Dimensions:** {plot_area_yd} Sq. Yards")
        st.write(f"**Total Architectural Area:** {total_built_up:,} Sq. Ft.") [cite: 207, 254]
        
    st.write("---")
    
    # Executive Philosophy Callout Box (Highly Elegant Line)
    st.markdown(f"<div style='background-color: #F4F7FA; border-left: 4px solid #1B365D; padding: 12px; font-style: italic; font-size:14px; color:#333;'>\"{custom_note}\"</div>", unsafe_allow_safe_html=True) [cite: 269]
    st.write("")
    
    # Floor-Wise Cost Breakup Section Table
    st.write("### **📋 DETAILED FINANCIAL COST BREAKUP**")
    
    # Generating standard columns for financial clarity
    th_col1, th_col2, th_col3, th_col4 = st.columns([2, 2, 2, 2])
    with th_col1: st.markdown("**Floor Profile**") [cite: 254]
    with th_col2: st.markdown("**Assigned Package**") [cite: 203]
    with th_col3: st.markdown("**Metrics (Area × Rate)**") [cite: 254]
    with th_col4: st.markdown("<p style='text-align:right;'><b>Net Amount (INR)</b></p>", unsafe_allow_safe_html=True) [cite: 254]
    st.markdown("<hr style='margin-top:2px; margin-bottom:6px;' />", unsafe_allow_safe_html=True)
    
    for item in floor_data:
        r_col1, r_col2, r_col3, r_col4 = st.columns([2, 2, 2, 2])
        f_cost = item['area'] * item['rate'] [cite: 254]
        with r_col1: st.write(item['floor']) [cite: 254]
        with r_col2: st.caption(item['package']) [cite: 203]
        with r_col3: st.write(f"{item['area']:,} Sq.ft @ ₹{item['rate']:,}") [cite: 254]
        with r_col4: st.markdown(f"<p style='text-align:right;'>₹ {f_cost:,.2f}</p>", unsafe_allow_safe_html=True) [cite: 254]
        
    st.write("---")
    
    # Net Financial Sum Block
    st.markdown(f"<h3 style='color: #1B365D; text-align: right;'>Total Construction Value: ₹ {net_project_cost:,.2f}</h3>", unsafe_allow_safe_html=True) [cite: 204, 254]
    st.markdown("<p style='text-align: right; font-size:11px; color:#777; margin-top:-10px;'>*Prices are system-generated commercial evaluations. Taxes extra as applicable.</p>", unsafe_allow_safe_html=True) [cite: 54, 109, 179, 255, 281]
    
    # Strategy / Additional Requirement Layout Notes
    st.write("### **⚙️ STRUCTURAL CONDITIONS & SPECIFICATIONS**")
    st.info(additional_reqs) [cite: 164, 216, 230, 257]
    
    # Standard Structural Technical Matrix Breakdowns
    st.markdown("**Core Brand Inclusions Across Architectural Scopes:**")
    st.markdown("""
    * **Structural Setup:** High-performance earthquake resilient framework layout using design mix concrete paired with premium Rathi Fe500 reinforcement steel grids[cite: 64, 128, 228, 229, 230].
    * **Masonry Standards:** Premium internal and external cement masonry applications executing AAC Block setups[cite: 17, 69, 128, 231].
    * **Finished Framework:** Detailed BOQ guidelines followed explicitly with continuous material tracking metrics[cite: 43, 96, 167, 262, 265].
    """)
    
    st.write("---")
    
    # Official Signature Footer
    f1, f2 = st.columns(2)
    with f1:
        st.write("")
        st.caption("Authorized Signatory") [cite: 279]
        st.write("**Shree Badree Build Tech Pvt. Ltd.**") [cite: 271, 280]
    with f2:
        st.markdown("<p style='text-align:right; font-size:11px; color:#555;'><b>Contact Core:</b> 8800614403, 9625803339<br><b>Email:</b> deeep1sharma@gmail.com</p>", unsafe_allow_safe_html=True) [cite: 50, 51, 104, 106, 175, 176]
        st.markdown("<p style='text-align:right; font-size:12px; color:#1B365D;'><b>Building Trust Through Quality & Transparency</b></p>", unsafe_allow_safe_html=True) [cite: 52, 108, 178, 277]
