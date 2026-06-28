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

# Mapping dropdown keys directly to match Excel column names
package_options = {
    "Solid Structure Core": "Core Shell Package", 
    "Essential Finishing": "Essential Package", 
    "Premium Luxury Profile": "Premium Luxury Package"
}

c_col1, c_col2 = st.columns(2)
with c_col1:
    client_name = st.text_input("Client Name", "Mr. & Mrs. Sharma")
    project_address = st.text_input("Site Location/Address", "Palam, Gurgaon (HR)")
    # GLOBAL SELECTION: Pure project ke liye ek hi master package selection
    selected_global_display = st.selectbox("Select Project Master Package", list(package_options.keys()), index=2)
    selected_excel_col = package_options[selected_global_display]

with c_col2:
    plot_area_yd = st.number_input("Plot Area (Sq. Yards)", min_value=10, max_value=2000, value=150)
    total_floors = st.slider("Number of Floors to Build (including Stilt/Ground)", min_value=1, max_value=6, value=3)

# AUTOMATIC PLOT AREA CONVERSION (1 Yard = 9 Sq.Ft)
plot_area_ft = plot_area_yd * 9

st.write("---")

# Section 2: Floor-Wise Detail Matrix Configuration (Rates Only)
st.subheader("📐 Step 2: Custom Floor Rates")
st.caption(f"Note: All floors are automatically assigned to **{selected_global_display}** with an area of **{plot_area_ft} Sq.Ft.**")

floor_data = []

# Dynamic rate configuration based on global package choice
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
        
    # Validation default rates based on global package selection
    if "Solid Structure" in selected_global_display:
        min_p, max_p, def_p = 1100, 1500, 1199
    elif "Essential" in selected_global_display:
        min_p, max_p, def_p = 1500, 2000, 1699
    else:
        min_p, max_p, def_p = 2000, 3000, 2399
        
    f_rate = st.number_input(f"Custom Rate for {floor_label} (₹/PSF)", min_value=min_p, max_value=max_p, value=def_p, key=f"rate_{i}")
    
    floor_data.append({
        "floor": floor_label, 
        "package": selected_global_display, 
        "area": plot_area_ft, 
        "rate": f_rate
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
net_project_cost = sum(item['area'] * item['rate'] for item in floor_data)

# 6. EXCEL SPECIFICATIONS GENERATION FOR HTML EMBED
excel_specs_html = ""
if df_matrix is not None:
    excel_specs_html += f"<div style='margin-top:15px; font-weight:bold; color:#1f2937;'>📦 Specifications Matrix for {selected_global_display}:</div><ul style='margin-top:5px; padding-left:20px; font-size:14px; color:#4b5563; line-height:1.6;'>"
    for idx, row in df_matrix.iterrows():
        category = row['Category / Element']
        spec_detail = row[selected_excel_col]
        if pd.notna(spec_detail) and "Excluded" not in str(spec_detail):
            excel_specs_html += f"<li><b>{category}:</b> {spec_detail}</li>"
    excel_specs_html += "</ul>"
else:
    excel_specs_html = "<p style='color:#ef4444; font-size:14px;'>ℹ️ Excel File (SBBT_Master_Quotation_Matrix.xlsx) not found in root path.</p>"

# 7. GENERATING PREMIUM PDF-STYLE HTML BREAKOUT (CRASH-PROOF & INLINE CALCULATION)
table_rows_html = ""
for item in floor_data:
    subtotal = item['area'] * item['rate']
    table_rows_html += f"""
    <tr style="border-bottom: 1px solid #e5e7eb;">
        <td style="padding: 10px; font-size: 14px; color: #1f2937; font-weight: 500;">{item['floor']}</td>
        <td style="padding: 10px; font-size: 14px; color: #4b5563;">{item['package']}</td>
        <td style="padding: 10px; font-size: 14px; color: #4b5563; text-align: center;">{item['area']:,} Sq.Ft</td>
        <td style="padding: 10px; font-size: 14px; color: #1f2937; text-align: right; font-weight: 600;">₹ {subtotal:,.2f} <span style="font-size:11px; color:#6b7280; font-weight:normal;">(@ ₹{item['rate']})</span></td>
    </tr>
    """

# MASTER HTML TEMPLATE CONTAINER
proposal_html = f"""
<div style="background-color: #ffffff; border: 2px solid #e5e7eb; border-radius: 8px; padding: 25px; font-family: 'Segoe UI', Arial, sans-serif; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
    
    <div style="text-align: center; border-bottom: 2px solid #111827; padding-bottom: 15px;">
        <h2 style="margin: 0; color: #111827; letter-spacing: 1px; font-size: 24px; font-weight: 700;">SHREE BADREE BUILD TECH PVT. LTD.</h2>
        <div style="font-size: 11px; color: #4b5563; margin-top: 4px; font-weight: 600; letter-spacing: 0.5px;">WHERE VISION MEETS PRECISION • TRUSTED SINCE 2011</div>
        <div style="font-size: 12px; color: #2563eb; font-weight: 500; margin-top: 2px;">⭐ Google Rating: 4.9/5.0 (50+ Happy Families)</div>
    </div>

    <div style="margin-top: 20px; display: flex; justify-content: space-between; font-size: 13px; line-height: 1.6; color: #374151;">
        <div style="flex: 1;">
            <b>Quotation Ref:</b> SBBT/Q/{datetime.date.today().year}/092<br>
            <b>Client Name:</b> {client_name}<br>
            <b>Project Site Location:</b> {project_address}
        </div>
        <div style="flex: 1; text-align: right;">
            <b>Date Issued:</b> {datetime.date.today().strftime('%d %B %Y')}<br>
            <b>Plot Size:</b> {plot_area_yd} Sq. Yards ({plot_area_ft} Sq. Ft.)<br>
            <b>Total Built-up Area:</b> {total_built_up:,} Sq. Ft. ({total_floors} Floors)
        </div>
    </div>

    <div style="margin-top: 20px; background-color: #f3f4f6; border-left: 4px solid #2563eb; padding: 12px; font-style: italic; font-size: 13px; color: #1f2937; border-radius: 0 4px 4px 0;">
        "{custom_note}"
    </div>

    <div style="margin-top: 25px;">
        <div style="font-weight: bold; font-size: 14px; margin-bottom: 8px; color: #111827;">📋 ITEM-WISE ARCHITECTURAL COST BREAKOUT:</div>
        <table style="width: 100%; border-collapse: collapse; text-align: left;">
            <thead>
                <tr style="background-color: #111827; color: #ffffff;">
                    <th style="padding: 10px; font-size: 13px; border-radius: 4px 0 0 0;">Floor Profile</th>
                    <th style="padding: 10px; font-size: 13px;">Selected Package</th>
                    <th style="padding: 10px; font-size: 13px; text-align: center;">Area (Sq.Ft)</th>
                    <th style="padding: 10px; font-size: 13px; text-align: right; border-radius: 0 4px 0 0;">Subtotal (INR)</th>
                </tr>
            </thead>
            <tbody>
                {table_rows_html}
            </tbody>
        </table>
    </div>

    <div style="margin-top: 20px; background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 6px; padding: 15px; display: flex; justify-content: space-between; align-items: center;">
        <span style="font-weight: bold; font-size: 14px; color: #1e40af;">TOTAL ESTIMATED CONSTRUCTION COST (Excl. GST):</span>
        <span style="font-size: 22px; font-weight: 700; color: #1e3a8a;">₹ {net_project_cost:,.2f}</span>
    </div>

    <div style="margin-top: 20px; background-color: #fffbeb; border: 1px solid #fde68a; border-radius: 6px; padding: 12px; font-size: 13px; color: #78350f;">
        <b>⚙️ STRUCTURAL EXTRA ADVANTAGES & COMMITMENTS:</b><br>
        <span style="color: #92400e;">{additional_reqs}</span>
    </div>

    <div style="margin-top: 20px; border-top: 1px dashed #d1d5db; padding-top: 15px;">
        {excel_specs_html}
    </div>

    <div style="margin-top: 20px; border-top: 1px dashed #d1d5db; padding-top: 15px; font-size: 12px; color: #4b5563; line-height: 1.5;">
        <b>🛡️ CORE STANDARD INCLUSIONS ACROSS ALL SCOPES:</b>
        <ul style="margin: 5px 0 0 0; padding-left: 18px;">
            <li><b>Heavy Duty Structural Core:</b> Complete RCC framework designed for highest seismic safety standards using RMC M25 Concrete and premium Rathi Fe500 steel layout.</li>
            <li><b>High-Grade Masonry:</b> Premium internal & external block work built with durable AAC Blocks or classic Red Bricks wrapped in rich cement mortar plaster.</li>
            <li><b>Quality Governance:</b> End-to-end transparent processing with detailed material checklists, continuous site monitoring, and formal project tracking.</li>
        </ul>
    </div>

    <div style="margin-top: 30px; border-top: 1px solid #111827; padding-top: 15px; display: flex; justify-content: space-between; font-size: 12px; color: #374151;">
        <div>
            <br>
            <span style="font-size: 11px; color: #6b7280; font-style: italic;">Authorized Signatory</span><br>
            <b>Shree Badree Build Tech Pvt. Ltd.</b>
        </div>
        <div style="text-align: right; line-height: 1.5;">
            📞 <b>Contact:</b> +91 8800614403, 9625803339<br>
            📧 <b>Email:</b> deeep1sharma@gmail.com<br>
            <span style="color: #6b7280; font-size:11px;">Building Trust Through Quality & Transparency</span>
        </div>
    </div>

</div>
"""

# 8. RENDER HTML PREVIEW SAFELY
st.write("---")
st.write("### 📈 SBBT Official Commercial Proposal")
st.caption("💡 Tip: Press **Ctrl + P** on this page to save or print this proposal as a clean corporate PDF.")

# Using safe native component to display the HTML Proposal (No refresh lag)
st.components.v1.html(proposal_html, height=1100, scroller=True)
