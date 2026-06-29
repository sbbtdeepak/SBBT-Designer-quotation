import streamlit as st
import pandas as pd
import datetime
import os

# 1. PAGE LAYOUT CONFIGURATION
st.set_page_config(page_title="SBBT Premium Quotation Engine", page_icon="🏗️", layout="centered")

# 2. AUTOMATIC & FLEXIBLE EXCEL SHEET READER
@st.cache_data
def load_sbbt_matrix():
    possible_files = ["SBBT_Master_Quotation_Matrix.xlsx", "SBBT_Master_Quotation_Matrix.XLSX", "sbbt_master_quotation_matrix.xlsx"]
    for file_name in possible_files:
        if os.path.exists(file_name):
            try:
                xl = pd.ExcelFile(file_name)
                sheet_target = "AI Master Matrix"
                if sheet_target not in xl.sheet_names:
                    sheet_target = xl.sheet_names[0]
                df = pd.read_excel(file_name, sheet_name=sheet_target)
                return df
            except Exception as e:
                continue
    return None

df_matrix = load_sbbt_matrix()

# 3. ADMIN GATEWAY SYSTEM
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("🏗️ SBBT Enterprise Portal")
    st.write("Shree Badree Build Tech Pvt. Ltd. — Administrative Login")
    
    with st.form("Access Portal"):
        username = st.text_input("Username", "sbbt_admin")
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

package_options = {
    "Solid Structure Core": "Core Shell Package", 
    "Essential Finishing": "Essential Package", 
    "Premium Luxury Profile": "Premium Luxury Package"
}

c_col1, c_col2 = st.columns(2)
with c_col1:
    client_name = st.text_input("Client Name", "Mr. & Mrs. Sharma")
    project_address = st.text_input("Site Location/Address", "Palam, Gurgaon (HR)")
    selected_global_display = st.selectbox("Select Project Master Package", list(package_options.keys()), index=2)
    selected_excel_col = package_options[selected_global_display]

with c_col2:
    plot_area_yd = st.number_input("Plot Area (Sq. Yards)", min_value=10, max_value=2000, value=150)
    total_floors = st.slider("Number of Floors to Build (including Stilt/Ground)", min_value=1, max_value=6, value=3)

plot_area_ft = plot_area_yd * 9

st.write("---")

# Section 2: Floor-Wise Detail Matrix Configuration (Rates Only)
st.subheader("📐 Step 2: Custom Floor Rates (GST Included)")
st.caption(f"Note: All floors are automatically assigned to **{selected_global_display}** with an area of **{plot_area_ft} Sq.Ft.**")

floor_data = []

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
        
    if "Solid Structure" in selected_global_display:
        min_p, max_p, def_p = 1100, 1500, 1199
    elif "Essential" in selected_global_display:
        min_p, max_p, def_p = 1500, 2000, 1699
    else:
        min_p, max_p, def_p = 2000, 3000, 2399
        
    f_rate = st.number_input(f"Custom Rate for {floor_label} (₹/PSF - GST Inc.)", min_value=min_p, max_value=max_p, value=def_p, key=f"rate_{i}")
    
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

# 6. DYNAMIC IMAGE CUTOUTS GENERATOR (Based on selection)
# Note: In production, you can replace these placeholder image links with real SBBT project image URLs.
images_html = "<div style='display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; margin-top: 15px; margin-bottom: 25px;'>"

if "Solid Structure" in selected_global_display:
    img_data = [
        {"title": "RCC Core Frame", "url": "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=150&h=150&fit=crop"},
        {"title": "Robust Brickwork", "url": "https://images.unsplash.com/photo-1590069261209-f8e9b8642343?w=150&h=150&fit=crop"},
        {"title": "Plaster Completed", "url": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?w=150&h=150&fit=crop"}
    ]
elif "Essential" in selected_global_display:
    img_data = [
        {"title": "Basic MS Gate Layout", "url": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=150&h=150&fit=crop"},
        {"title": "Premium Internal Doors", "url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=150&h=150&fit=crop"},
        {"title": "Modern Front Elevation", "url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=150&h=150&fit=crop"}
    ]
else: # Premium Luxury
    img_data = [
        {"title": "Modular Luxury Kitchen", "url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=150&h=150&fit=crop"},
        {"title": "Designer Wardrobes", "url": "https://images.unsplash.com/photo-1558882224-cca166733360?w=150&h=150&fit=crop"},
        {"title": "Heavy Glass Railings", "url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=150&h=150&fit=crop"},
        {"title": "Wall-Hung WC & Diverter", "url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=150&h=150&fit=crop"},
        {"title": "Automatic Elevator", "url": "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=150&h=150&fit=crop"},
        {"title": "Bespoke False Ceiling", "url": "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=150&h=150&fit=crop"}
    ]

for img in img_data:
    images_html += f"""
    <div style="text-align: center; width: 120px;">
        <img src="{img['url']}" style="width: 100px; height: 100px; border-radius: 50%; object-fit: cover; border: 3px solid #2563eb; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" alt="{img['title']}">
        <div style="font-size: 11px; font-weight: 600; margin-top: 6px; color: #374151; line-height: 1.2;">{img['title']}</div>
    </div>
    """
images_html += "</div>"

# 7. BRANDS WE WORK WITH BLOCK
brands_list = [
    "Somany", "Nitco", "Kajaria", "Jaquar", "Hindware", "Cera", "Tata Tiscon", "Sail", 
    "Kangaroo Ply", "Chivas Ply", "Havells", "Polycab", "Greenply", "Sainik Door", 
    "Plaza Locks", "Godrej Locks", "Century Ply", "Astral Pipes", "Orient Electric", "Syntex"
]
brands_html = "<div style='margin-top: 25px; border-top: 2px solid #e5e7eb; padding-top: 15px;'>"
brands_html += "<div style='font-weight: bold; font-size: 14px; color: #111827; margin-bottom: 10px; letter-spacing: 0.5px;'>🤝 PREMIUM ECOSYSTEM BRANDS WE TRUST & WORK WITH:</div>"
brands_html += "<div style='display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-start;'>"
for brand in brands_list:
    brands_html += f"<span style='background-color: #f3f4f6; color: #1f2937; padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; border: 1px solid #e5e7eb;'>{brand}</span>"
brands_html += "</div></div>"

# 8. DYNAMIC EXCEL MATERIAL SPECIFICATIONS FETCHING WITH INTERACTIVE FALLBACKS
excel_specs_html = ""
if df_matrix is not None and selected_excel_col in df_matrix.columns:
    excel_specs_html += f"<div style='margin-top:15px; font-weight:bold; color:#111827;'>🛡️ MATERIAL SPECIFICATIONS MATRIX FOR {selected_global_display.upper()} (LIVE FROM EXCEL):</div><ul style='margin-top:8px; padding-left:20px; font-size:14px; color:#374151; line-height:1.6;'>"
    for idx, row in df_matrix.iterrows():
        category = row['Category / Element'] if 'Category / Element' in df_matrix.columns else row.iloc[0]
        spec_detail = row[selected_excel_col]
        if pd.notna(spec_detail) and "Excluded" not in str(spec_detail):
            excel_specs_html += f"<li><b>{category}:</b> {spec_detail}</li>"
    excel_specs_html += "</ul>"
else:
    excel_specs_html += f"<div style='margin-top:15px; font-weight:bold; color:#111827;'>🛡️ DETAILED MATERIAL SPECIFICATIONS MATRIX ({selected_global_display.upper()}):</div>"
    excel_specs_html += "<ul style='margin-top:8px; padding-left:20px; font-size:14px; color:#374151; line-height:1.6;'>"
    if "Solid Structure" in selected_global_display:
        excel_specs_html += "<li><b>Scope Definition:</b> Pure Structural Grey Structure Core (Brickwork, RCC, Plastering only).</li>"
        excel_specs_html += "<li><b>Steel Layout:</b> Heavy Duty Rathi Fe500 / Kamdhenu structural reinforcement layout.</li>"
        excel_specs_html += "<li><b>Concrete Grade:</b> Certified M25 Design Mix RMC for columns, beams, and foundations.</li>"
    elif "Essential" in selected_global_display:
        excel_specs_html += "<li><b>Scope Definition:</b> Structural Framework combined with Standard Functional Finishing Layout.</li>"
        excel_specs_html += "<li><b>Flooring Profiles:</b> Premium Vitrified tiles (2x2 or 4x2) in living areas and anti-skid floor setups.</li>"
    else:
        excel_specs_html += "<li><b>Front Elevation:</b> Dynamic Modern HPL Cladding & ACP Sheet architectural framework.</li>"
        excel_specs_html += "<li><b>Vertical Transit:</b> Premium 4-Passenger Automatic Elevator completely embedded.</li>"
        excel_specs_html += "<li><b>Balconies & Stairs:</b> Heavy SS304 Top-Rail Glass Railing for 5 front layout openings.</li>"
    excel_specs_html += "</ul>"

# 9. GENERATING LIVE BREAKOUT ROWS
table_rows_html = ""
for item in floor_data:
    subtotal = item['area'] * item['rate']
    table_rows_html += f"""
    <tr style="border-bottom: 1px solid #e5e7eb;">
        <td style="padding: 12px; font-size: 14px; color: #111827; font-weight: 500;">{item['floor']}</td>
        <td style="padding: 12px; font-size: 14px; color: #4b5563;">{item['package']}</td>
        <td style="padding: 12px; font-size: 14px; color: #4b5563; text-align: center;">{item['area']:,} Sq.Ft</td>
        <td style="padding: 12px; font-size: 14px; color: #111827; text-align: right; font-weight: 600;">₹ {subtotal:,.2f} <span style="font-size:11px; color:#6b7280; font-weight:normal;">(Inc. GST)</span></td>
    </tr>
    """

# MASTER PROPOSAL HTML CONTAINER
proposal_html = f"""
<div style="background-color: #ffffff; border: 2px solid #d1d5db; border-radius: 8px; padding: 30px; font-family: 'Segoe UI', Arial, sans-serif; color: #111827; max-width: 850px; margin: 0 auto; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
    
    <div style="text-align: center; border-bottom: 3px solid #111827; padding-bottom: 15px;">
        <h2 style="margin: 0; color: #111827; letter-spacing: 1px; font-size: 26px; font-weight: 700;">SHREE BADREE BUILD TECH PVT. LTD.</h2>
        <div style="font-size: 12px; color: #4b5563; margin-top: 5px; font-weight: 600; letter-spacing: 0.5px;">WHERE VISION MEETS PRECISION • TRUSTED SINCE 2011</div>
        <div style="font-size: 13px; color: #2563eb; font-weight: 500; margin-top: 3px;">⭐ Google Rating: 4.9/5.0 (50+ Happy Families)</div>
    </div>

    <div style="margin-top: 22px; display: flex; justify-content: space-between; font-size: 14px; line-height: 1.6; color: #374151;">
        <div style="width: 50%;">
            <b>Quotation Ref:</b> SBBT/Q/{datetime.date.today().year}/092<br>
            <b>Client Name:</b> {client_name}<br>
            <b>Project Site Location:</b> {project_address}
        </div>
        <div style="width: 50%; text-align: right;">
            <b>Date Issued:</b> {datetime.date.today().strftime('%d %B %Y')}<br>
            <b>Plot Size:</b> {plot_area_yd} Sq. Yards ({plot_area_ft} Sq. Ft.)<br>
            <b>Total Built-up Area:</b> {total_built_up:,} Sq. Ft. ({total_floors} Floors)
        </div>
    </div>

    <div style="margin-top: 22px; background-color: #f3f4f6; border-left: 4px solid #2563eb; padding: 15px; font-style: italic; font-size: 14px; color: #1f2937; border-radius: 0 4px 4px 0;">
        "{custom_note}"
    </div>

    <!-- DYNAMIC VISUAL CUTOUTS INJECTED HERE -->
    <div style="margin-top: 25px; border: 1px solid #e5e7eb; border-radius: 6px; padding: 15px; background-color: #fafafa;">
        <div style="font-weight: bold; font-size: 14px; color: #111827; margin-bottom: 10px; text-align: center; letter-spacing: 0.5px;">📸 ON-SITE WORK & MATERIAL DELIVERY HIGHLIGHTS:</div>
        {images_html}
    </div>

    <div style="margin-top: 25px;">
        <div style="font-weight: bold; font-size: 15px; margin-bottom: 10px; color: #111827;">📋 ITEM-WISE ARCHITECTURAL COST BREAKOUT:</div>
        <table style="width: 100%; border-collapse: collapse; text-align: left;">
            <thead>
                <tr style="background-color: #111827; color: #ffffff;">
                    <th style="padding: 12px; font-size: 14px;">Floor Profile</th>
                    <th style="padding: 12px; font-size: 14px;">Selected Package</th>
                    <th style="padding: 12px; font-size: 14px; text-align: center;">Area (Sq.Ft)</th>
                    <th style="padding: 12px; font-size: 14px; text-align: right;">Subtotal (INR)</th>
                </tr>
            </thead>
            <tbody>
                {table_rows_html}
            </tbody>
        </table>
    </div>

    <div style="margin-top: 25px; background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 6px; padding: 18px; display: flex; justify-content: space-between; align-items: center;">
        <span style="font-weight: bold; font-size: 15px; color: #1e40af;">TOTAL ESTIMATED CONSTRUCTION COST (GST INCLUDED):</span>
        <span style="font-size: 24px; font-weight: 700; color: #1e3a8a;">₹ {net_project_cost:,.2f}</span>
    </div>

    <div style="margin-top: 22px; background-color: #fffbeb; border: 1px solid #fde68a; border-radius: 6px; padding: 15px; font-size: 14px; color: #78350f;">
        <b>⚙️ STRUCTURAL EXTRA ADVANTAGES & COMMITMENTS:</b><br>
        <span style="color: #92400e; display: block; margin-top: 5px;">{additional_reqs}</span>
    </div>

    <div style="margin-top: 25px; border-top: 1px dashed #cfd5db; padding-top: 20px;">
        {excel_specs_html}
    </div>

    <!-- BRANDS ECOSYSTEM SECTION -->
    {brands_html}

    <div style="margin-top: 25px; border-top: 1px dashed #cfd5db; padding-top: 20px; font-size: 13px; color: #4b5563; line-height: 1.6;">
        <b>🛡️ CORE STANDARD INCLUSIONS ACROSS ALL SCOPES:</b>
        <ul style="margin: 6px 0 0 0; padding-left: 20px;">
            <li><b>Heavy Duty Structural Core:</b> Complete RCC framework designed for highest seismic safety standards using RMC M25 Concrete and premium Rathi Fe500 steel layout.</li>
            <li><b>High-Grade Masonry:</b> Premium internal & external block work built with durable AAC Blocks or classic Red Bricks wrapped in rich cement mortar plaster.</li>
        </ul>
    </div>

    <div style="margin-top: 35px; border-top: 2px solid #111827; padding-top: 20px; display: flex; justify-content: space-between; font-size: 13px; color: #374151;">
        <div>
            <br>
            <span style="font-size: 12px; color: #6b7280; font-style: italic;">Authorized Signatory</span><br>
            <b>Shree Badree Build Tech Pvt. Ltd.</b>
        </div>
        <div style="text-align: right; line-height: 1.6;">
            📞 <b>Contact:</b> +91 8800614403, 9625803339<br>
            📧 <b>Email:</b> deeep1sharma@gmail.com<br>
            <span style="color: #6b7280; font-size: 12px;">Building Trust Through Quality & Transparency</span>
        </div>
    </div>

</div>
"""

# HTML Download Wrapper
full_html_page = f"<!DOCTYPE html><html><head><meta charset='utf-8'></head><body style='margin:0; padding:20px; background-color:#ffffff;'>{proposal_html}</body></html>"

# 10. LIVE DASHBOARD INTERFACE
st.write("---")
st.write("### 📈 SBBT Official Commercial Proposal")

st.download_button(
    label="📥 Download Designer Proposal (.html)",
    data=full_html_page,
    file_name="SBBT_Official_Quotation.html",
    mime="text/html",
    type="primary"
)

st.write("")
st.markdown(proposal_html, unsafe_allow_html=True)
