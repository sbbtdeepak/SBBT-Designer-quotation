import streamlit as st
import pandas as pd
import datetime
import os

# 1. PAGE SETUP
st.set_page_config(page_title="SBBT Executive Proposal Engine", page_icon="🏗️", layout="centered")

# 2. AUTOMATIC MATRIX LOADER
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
                return pd.read_excel(file_name, sheet_name=sheet_target)
            except Exception:
                continue
    return None

df_matrix = load_sbbt_matrix()

# 3. AUTHENTICATION GATEWAY
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("🏗️ SBBT Enterprise Portal")
    st.write("Shree Badree Build Tech Pvt. Ltd. — Administrative Login")
    with st.form("Access Portal"):
        username = st.text_input("Username", "sbbt_admin")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Authenticate Entry"):
            if username == "sbbt_admin" and password == "sbbt@2026":
                st.session_state['authenticated'] = True
                st.rerun()
            else:
                st.error("Access Denied: Invalid Administrative Credentials")
    st.stop()

# 4. ENGINE CONTROLS
st.title("🎛️ SBBT Ultra-Premium Estimation Control")
st.write("---")

package_options = {
    "Solid Structure Core": "Core Shell Package", 
    "Essential Finishing": "Essential Package", 
    "Premium Luxury Profile": "Premium Luxury Package"
}

col1, col2 = st.columns(2)
with col1:
    client_name = st.text_input("Client Name", "Mr. & Mrs. Sharma")
    project_address = st.text_input("Site Location/Address", "Palam, Gurgaon (HR)")
    selected_global_display = st.selectbox("Select Master Package", list(package_options.keys()), index=2)
    selected_excel_col = package_options[selected_global_display]

with col2:
    plot_area_yd = st.number_input("Plot Area (Sq. Yards)", min_value=10, max_value=2000, value=150)
    total_floors = st.slider("Number of Floors", min_value=1, max_value=6, value=3)

plot_area_ft = plot_area_yd * 9
total_built_up = plot_area_ft * total_floors

st.write("---")
st.subheader("📐 Custom Floor Pricing Setup")

floor_data = []
for i in range(total_floors):
    floor_label = "Ground Floor / Stilt" if i == 0 else "First Floor" if i == 1 else "Second Floor" if i == 2 else "Third Floor" if i == 3 else f"{i}th Floor"
    
    if "Solid Structure" in selected_global_display:
        min_p, max_p, def_p = 1100, 1500, 1199
    elif "Essential" in selected_global_display:
        min_p, max_p, def_p = 1500, 2000, 1699
    else:
        min_p, max_p, def_p = 2000, 3000, 2399
        
    f_rate = st.number_input(f"Rate for {floor_label} (₹/PSF - GST Inc.)", min_value=min_p, max_value=max_p, value=def_p, key=f"rate_{i}")
    floor_data.append({"floor": floor_label, "area": plot_area_ft, "rate": f_rate})

st.write("---")
custom_note = st.text_area("Client Dedication Note", "We are offering a special commercial advantage for your property while maintaining premium specifications and long-term value, ensuring trust with zero compromises.")
additional_reqs = st.text_area("Extra Strategic Commitments", "Includes 15+ luxury upgrades, earthquake resistant RCC frame configuration, and a comprehensive 2-Year AMC covering operational support.")

# MATHEMATICAL COMPUTATION
net_project_cost = sum(item['area'] * item['rate'] for item in floor_data)

# 5. IMAGE CONFIGURATION
images_html = ""
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
else:
    img_data = [
        {"title": "Modular Luxury Kitchen", "url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=150&h=150&fit=crop"},
        {"title": "Designer Wardrobes", "url": "https://images.unsplash.com/photo-1558882224-cca166733360?w=150&h=150&fit=crop"},
        {"title": "Heavy Glass Railings", "url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=150&h=150&fit=crop"},
        {"title": "Wall-Hung WC Layout", "url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=150&h=150&fit=crop"},
        {"title": "Automatic Elevator", "url": "https://images.unsplash.com/photo-1563986768609-322da13575f3?w=150&h=150&fit=crop"},
        {"title": "Bespoke False Ceiling", "url": "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=150&h=150&fit=crop"}
    ]

for img in img_data:
    images_html += f"""
    <div style="text-align: center; width: 110px;">
        <img src="{img['url']}" style="width: 85px; height: 85px; border-radius: 12px; object-fit: cover; border: 2px solid #2563eb;" alt="{img['title']}">
        <div style="font-size: 11px; font-weight: 600; margin-top: 6px; color: #374151;">{img['title']}</div>
    </div>"""

# 6. BRANDS ECOSYSTEM
brands_list = ["Somany", "Nitco", "Kajaria", "Jaquar", "Hindware", "Cera", "Tata Tiscon", "Sail", "Kangaroo Ply", "Chivas Ply", "Havells", "Polycab", "Greenply", "Sainik Door", "Plaza Locks", "Godrej Locks", "Century Ply", "Astral Pipes", "Orient Electric", "Syntex"]
brands_html = "".join([f"<span style='background-color: #f3f4f6; color: #1f2937; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 600; border: 1px solid #e5e7eb;'>{b}</span> " for b in brands_list])

# 7. MATRICES FROM EXCEL / FALLBACK
excel_specs_html = ""
if df_matrix is not None and selected_excel_col in df_matrix.columns:
    for idx, row in df_matrix.iterrows():
        cat = row['Category / Element'] if 'Category / Element' in df_matrix.columns else row.iloc[0]
        spec = row[selected_excel_col]
        if pd.notna(spec) and "Excluded" not in str(spec):
            excel_specs_html += f"<li><b>{cat}:</b> {spec}</li>"
else:
    if "Solid Structure" in selected_global_display:
        excel_specs_html += "<li><b>Scope Definition:</b> Pure Structural Grey Structure Core Layout.</li><li><b>Concrete Grade:</b> Certified M25 Design Mix RMC Structure.</li>"
    elif "Essential" in selected_global_display:
        excel_specs_html += "<li><b>Scope Definition:</b> Structural Framework combined with Standard Functional Finishing.</li><li><b>Flooring:</b> Premium Vitrified Tiles (600x600 mm).</li>"
    else:
        excel_specs_html += "<li><b>Front Elevation:</b> Dynamic Modern HPL Cladding & ACP Sheet Framework.</li><li><b>Vertical Transit:</b> Premium 4-Passenger Automatic Elevator.</li><li><b>Finishing:</b> Heavy SS304 Top-Rail Glass Railing layout.</li>"

# 8. TABLE DATA ROWS
table_rows_html = ""
for item in floor_data:
    subtotal = item['area'] * item['rate']
    table_rows_html += f"""
    <tr style="border-bottom: 1px solid #e5e7eb;">
        <td style="padding: 10px; font-size: 13px; color: #111827; font-weight: 500;">{item['floor']}</td>
        <td style="padding: 10px; font-size: 13px; color: #4b5563; text-align: center;">{item['area']:,} Sq.Ft</td>
        <td style="padding: 10px; font-size: 13px; color: #111827; text-align: right; font-weight: 600;">\u20b9 {subtotal:,.2f}</td>
    </tr>"""

# 9. CONSTRUCTING SAFE STRINGS (Isolating JS script from Python formatting blocks)
proposal_template = """
<div style="background-color: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 35px; font-family: 'Segoe UI', Arial, sans-serif; color: #111827; max-width: 800px; margin: 0 auto; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05);">
    
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #111827; padding-bottom: 15px;">
        <div>
            <h2 style="margin: 0; color: #111827; font-size: 22px; font-weight: 800; letter-spacing: 0.5px;">SHREE BADREE BUILD TECH PVT. LTD.</h2>
            <div style="font-size: 11px; color: #6b7280; font-weight: 600; margin-top: 3px;">WHERE VISION MEETS PRECISION • TRUSTED PARTNER</div>
        </div>
        <div style="text-align: right; background-color: #f3f4f6; padding: 6px 12px; border-radius: 8px;">
            <span style="font-size: 12px; font-weight: 700; color: #2563eb;">⭐ Google Rating: 4.9/5.0</span>
        </div>
    </div>

    <div style="margin-top: 20px; display: flex; justify-content: space-between; font-size: 13px; color: #374151; line-height: 1.5;">
        <div>
            <b>Quotation Ref:</b> SBBT/Q/2026/092<br>
            <b>Client Name:</b> {client_name}<br>
            <b>Project Location:</b> {project_address}
        </div>
        <div style="text-align: right;">
            <b>Date Issued:</b> {date_issued}<br>
            <b>Plot Size:</b> {plot_area_yd} Yd ({plot_area_ft} Sq.Ft)<br>
            <b>Total Floors:</b> {total_floors} Floors ({total_built_up:,} Built-up PSF)
        </div>
    </div>

    <div style="margin-top: 15px; background-color: #fafafa; border-left: 3px solid #2563eb; padding: 12px; font-style: italic; font-size: 13px; color: #4b5563; border-radius: 0 6px 6px 0;">
        "{custom_note}"
    </div>

    <div style="margin-top: 20px; border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px; background-color: #ffffff;">
        <div style="font-weight: 700; font-size: 12px; color: #111827; margin-bottom: 12px; text-align: center; letter-spacing: 0.5px; text-transform: uppercase;">📸 On-Site Execution Scope Framework:</div>
        <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
            {images_html}
        </div>
    </div>

    <div style="margin-top: 15px; background-color: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px;">
        <div style="font-weight: 700; font-size: 11px; color: #374151; margin-bottom: 8px; text-transform: uppercase;">🤝 Trusted Material Ecosystem Brands:</div>
        <div style="display: flex; flex-wrap: wrap; gap: 6px;">
            {brands_html}
        </div>
    </div>

    <div style="margin-top: 20px;">
        <table style="width: 100%; border-collapse: collapse; text-align: left;">
            <thead>
                <tr style="background-color: #111827; color: #ffffff;">
                    <th style="padding: 10px; font-size: 13px;">Floor Profile Matrix</th>
                    <th style="padding: 10px; font-size: 13px; text-align: center;">Built Area</th>
                    <th style="padding: 10px; font-size: 13px; text-align: right;">Subtotal (INR)</th>
                </tr>
            </thead>
            <tbody>
                {table_rows_html}
            </tbody>
        </table>
    </div>

    <div style="margin-top: 20px; background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 15px; display: flex; justify-content: space-between; align-items: center;">
        <span style="font-weight: 700; font-size: 13px; color: #1e40af; letter-spacing: 0.3px;">TOTAL ESTIMATED CONSTRUCTION INVESTMENT (GST INCLUDED):</span>
        <span style="font-size: 20px; font-weight: 800; color: #1e3a8a;">\u20b9 {net_project_cost:,.2f}</span>
    </div>

    <div style="margin-top: 15px; background-color: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 12px; font-size: 13px; color: #78350f;">
        <b>⚡ Executive Special Commitments & Guarantees:</b>
        <div style="color: #92400e; margin-top: 4px; font-size: 12px;">{additional_reqs}</div>
    </div>

    <div style="margin-top: 20px; border-top: 1px dashed #e5e7eb; padding-top: 15px;">
        <div style="font-weight:700; font-size: 13px; color:#111827; margin-bottom: 6px;">🛡️ CORE PACK ARCHITECTURAL TECHNICAL SPECIFICATIONS:</div>
        <ul style="padding-left:18px; font-size:12px; color:#4b5563; line-height: 1.5; margin: 0;">
            {excel_specs_html}
        </ul>
    </div>

    <div style="margin-top: 30px; border-top: 2px solid #111827; padding-top: 15px; display: flex; justify-content: space-between; font-size: 12px; color: #4b5563;">
        <div>
            <br>
            <span style="font-size: 11px; color: #9ca3af; font-style: italic;">Authorized Signatory</span><br>
            <b>Shree Badree Build Tech Pvt. Ltd.</b>
        </div>
        <div style="text-align: right; line-height: 1.4;">
            📞 +91 8800614403, 9625803339<br>
            📧 deeep1sharma@gmail.com<br>
            <span style="color: #2563eb; font-weight: 600;">Building Trust with Complete Transparency</span>
        </div>
    </div>

</div>
"""

proposal_html = proposal_template.format(
    client_name=client_name,
    project_address=project_address,
    date_issued=datetime.date.today().strftime('%d %B %Y'),
    plot_area_yd=plot_area_yd,
    plot_area_ft=plot_area_ft,
    total_floors=total_floors,
    total_built_up=total_built_up,
    custom_note=custom_note,
    images_html=images_html,
    brands_html=brands_html,
    table_rows_html=table_rows_html,
    net_project_cost=net_project_cost,
    additional_reqs=additional_reqs,
    excel_specs_html=excel_specs_html
)

# PRINT CONTROLLER VIA EMBEDDED JAVASCRIPT WINDOW
full_html_page = """<!DOCTYPE html><html><head><meta charset='utf-8'></head>
<body style='margin:0; padding:20px; background-color:#ffffff;'>
{}
<script>window.onload = function() {{ window.print(); }};</script>
</body></html>""".format(proposal_html)

# 10. UI PRESENTATION GATEWAY
st.write("### 💎 Live Executive Proposal Preview")
st.caption("Neeche click karke direct proposal save ya print kar sakte hain:")

st.download_button(
    label="🖨️ Generate & Save Official PDF",
    data=full_html_page,
    file_name=f"SBBT_Premium_Quotation_{client_name.replace(' ', '_')}.html",
    mime="text/html",
    type="primary"
)

st.write("")
st.markdown(proposal_html, unsafe_allow_html=True)
