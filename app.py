import streamlit as st
import pandas as pd
import datetime

# 1. PAGE LAYOUT CONFIGURATION
st.set_page_config(page_title="SBBT Premium Quotation Engine", page_icon="🏗️", layout="centered")

# 2. BACKGROUND ENGINE: EXCEL SHEET READER
@st.cache_data
def load_sbbt_matrix():
    try:
        df = pd.read_excel("SBBT_Master_Quotation_Matrix.xlsx", sheet_name="AI Master Matrix")
        return df
    except Exception as e:
        return None

df_matrix = load_sbbt_matrix()

# 3. ADMIN GATEWAY SYSTEM
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

# 4. EXECUTIVE CONTROL PANEL
st.title("🎛️ SBBT Premium Estimation Panel")
st.write("---")

# Section 1: Client Profile Matrix & Global Package Selection
st.subheader("👤 Step 1: Project & Package Profile")

# Mapping dropdown keys directly to match your Excel column names exactly
package_options = {
    "Solid Structure Core (₹1199)": "Core Shell Package", 
    "Essential Finishing (₹1699)": "Essential Package", 
    "Premium Luxury Profile (₹2099)": "Premium Luxury Package"
}

c_col1, c_col2 = st.columns(2)
with c_col1:
    client_name = st.text_input("Client Name", "Mr. & Mrs. Sharma")
    project_address = st.text_input("Site Location/Address", "Palam, Gurgaon (HR)")
    # SHIFTED UP: Global package selection for all floors
    selected_global_display = st.selectbox("Select Master Project Package", list(package_options.keys()), index=2)
    selected_excel_col = package_options[selected_global_display]

with c_col2:
    plot_area_yd = st.number_input("Plot Area (Sq. Yards)", min_value=10, max_value=2000, value=150)
    total_floors = st.slider("Number of Floors to Build (including Stilt/Ground)", min_value=1, max_value=6, value=3)

# AUTOMATIC PLOT AREA CONVERSION (1 Yard = 9 Sq.Ft)
plot_area_ft = plot_area_yd * 9

st.write("---")

# Section 2: Floor-Wise Detail Matrix Configuration (Rates Only)
st.subheader("📐 Step 2: Custom Floor Rates")
st.caption(f"Note: All floors are automatically assigned to **{selected_global_display.split(' (')[0]}** with an area of **{plot_area_ft} Sq.Ft.**")

floor_data = []

# Dynamic rate configuration fields based on global package choice
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
        
    # Standard base validation check based on the choice from top
    if "Solid Structure" in selected_global_display:
        min_p, max_p, def_p = 1100, 1500, 1199
    elif "Essential" in selected_global_display:
        min_p, max_p, def_p = 1500, 2000, 1699
    else:
        min_p, max_p, def_p = 2000, 3000, 2399
        
    f_rate = st.number_input(f"Custom Rate for {floor_label} (₹/PSF)", min_value=min_p, max_value=max_p, value=def_p, key=f"rate_{i}")
    
    floor_data.append({
        "Floor Profile": floor_label, 
        "Package Profile": selected_global_display.split(" (")[0], 
        "Area (Sq.Ft)": plot_area_ft, 
        "Rate (₹/PSF)": f_rate
    })

st.write("---")

# Section 3: Notes & Personalization
st.subheader("✍️ Step 3: Executive Customization & Strategy Notes")
custom_note = st.text_area(
    "Custom Dedication Line (Client-Centric Touch)", 
    f"We are offering a special commercial advantage for your property at {project_address} while maintaining premium specifications and long-term value, ensuring trust with zero compromises."
)
additional_reqs = st.text_area("Additional Requirements / Custom Structural Commitments", "Includes 15+ luxury upgrades, earthquake resistant RCC frame configuration, and a comprehensive 2-Year AMC covering operational support.")

# 5. MATHEMATICAL COMPUTATION
total_built_up = plot_area_ft * total_floors
net_project_cost = sum(item['Area (Sq.Ft)'] * item['Rate (₹/PSF)'] for item in floor_data)

# Convert data to clean DataFrame for breakout view
df_display = pd.DataFrame(floor_data)
df_display["Subtotal Amount (INR)"] = df_display["Area (Sq.Ft)"] * df_display["Rate (₹/PSF)"]
df_display["Subtotal Amount (INR)"] = df_display["Subtotal Amount (INR)"].map("₹ {:,.2f}".format)

# 6. ELEGANT EXECUTIVE PROPOSAL DISPLAY
st.write("---")
st.write("### 📈 SBBT Official Commercial Proposal")
st.caption("💡 Tip: Click on the preview block below and press **Ctrl + P** to save or print cleanly.")

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
    st.dataframe(df_display, hide_index=True, use_container_width=True)
        
    st.write("")
    st.metric(label="TOTAL ESTIMATED CONSTRUCTION COST (Excl. GST)", value=f"₹ {net_project_cost:,.2f}")
    st.write("---")
    
    # Section: Strategy & Commitments
    st.write("**⚙️ STRUCTURAL EXTRA ADVANTAGES & COMMITMENTS:**")
    st.warning(additional_reqs)
    st.write("---")
    
    # DYNAMIC EXCEL MATERIAL SPECIFICATIONS FETCHING
    st.write("**🛡️ DETAILED MATERIAL SPECIFICATIONS MATRIX (FROM EXCEL):**")
    
    if df_matrix is not None:
        st.markdown(f"### 📦 Specifications for **{selected_global_display.split(' (')[0]}**:")
        
        for idx, row in df_matrix.iterrows():
            category = row['Category / Element']
            spec_detail = row[selected_excel_col]
            
            if pd.notna(spec_detail) and "Excluded" not in str(spec_detail):
                st.markdown(f"* **{category}:** {spec_detail}")
    else:
        st.info("ℹ️ Excel Data Stream offline hai. Please check karein ki 'SBBT_Master_Quotation_Matrix.xlsx' root repository folder me uploaded hai.")

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
