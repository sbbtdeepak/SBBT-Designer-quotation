import streamlit as st
import pandas as pd
import datetime
import os

# 1. PAGE SETUP
st.set_page_config(page_title="SBBT Executive Proposal Engine", page_icon="🏗️", layout="centered")

# IMAGE CONFIGURATION HELPER
def get_image_source(file_name, fallback_url):
    """
    Agar 'images' folder mein local file milti hai toh use static asset ki tarah lift karega,
    nahi toh fallback cloud URL chalega.
    """
    local_path = os.path.join("images", file_name)
    if os.path.exists(local_path):
        return local_path
    return fallback_url

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
    plot_area_yd = st.number_input("Plot Area Reference (Sq. Yards)", min_value=10, max_value=2000, value=150)
    total_floors = st.slider("Number of Floors to Configure", min_value=1, max_value=6, value=3)

plot_area_ft_ref = plot_area_yd * 9

st.write("---")
# DYNAMIC USER FLOOR-WISE ENTRY
st.subheader("📐 Step 2: Custom Floor Layout & Area Configuration")
st.caption("Aap har floor ka Built-up Area, Layout Details (Text) aur Rate khud customize kar sakte hain:")

floor_data = []
total_built_up = 0.0

for i in range(total_floors):
    floor_label = "Ground Floor / Stilt" if i == 0 else "First Floor" if i == 1 else "Second Floor" if i == 2 else "Third Floor" if i == 3 else f"{i}th Floor"
    
    st.markdown(f"#### 🏢 {floor_label}")
    fl_col1, fl_col2, fl_col3 = st.columns([1.5, 1.5, 1.5])
    
    with fl_col1:
        f_area = st.number_input(f"Built Area (Sq.Ft)", min_value=50, max_value=10000, value=int(plot_area_ft_ref), key=f"area_val_{i}")
    
    with fl_col2:
        f_layout = st.text_input(f"Layout Configuration", value="3 BHK with Attach Bathroom" if i > 0 else "Stilt Parking + 1 Office", key=f"layout_val_{i}")
        
    with fl_col3:
        if "Solid Structure" in selected_global_display:
            min_p, max_p, def_p = 1100, 1500, 1199
        elif "Essential" in selected_global_display:
            min_p, max_p, def_p = 1500, 2000, 1659
        else:
            min_p, max_p, def_p = 2000, 3000, 2400
        f_rate = st.number_input(f"Rate (Rs/PSF - GST Inc.)", min_value=min_p, max_value=max_p, value=def_p, key=f"rate_val_{i}")
        
    floor_data.append({"floor": floor_label, "area": f_area, "layout": f_layout, "rate": f_rate})
    total_built_up += f_area

st.write("---")
custom_note = st.text_area("Client Dedication Note", "We are offering a special commercial advantage for your property while maintaining premium specifications and long-term value, ensuring trust with zero compromises.")
additional_reqs = st.text_area("Extra Strategic Commitments", "Includes specialized brand structural alignments, earthquake resistant RCC frame configuration, and comprehensive support services.")

# MATHEMATICAL COMPUTATION
net_project_cost = sum(item['area'] * item['rate'] for item in floor_data)

# 5. DYNAMIC NEW IMAGE DESIGN SECTION (Categorized exactly as per your specification)
images_html = ""
if "Solid Structure" in selected_global_display:
    img_data = [
        {"title": "RCC Core Frame", "file": "rcc_frame.jpg", "url": "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=150&h=150&fit=crop"},
        {"title": "Robust Brickwork", "file": "brickwork.jpg", "url": "https://images.unsplash.com/photo-1590069261209-f8e9b8642343?w=150&h=150&fit=crop"},
        {"title": "Plaster Completed", "file": "plaster.jpg", "url": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?w=150&h=150&fit=crop"}
    ]
elif "Essential" in selected_global_display:
    img_data = [
        {"title": "MS Main Gate", "file": "ms_main_gate.jpg", "url": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=150&h=150&fit=crop"},
        {"title": "MS Railing", "file": "ms_railing.jpg", "url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=150&h=150&fit=crop"},
        {"title": "Flush Door", "file": "flush_door.jpg", "url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=150&h=150&fit=crop"},
        {"title": "Designer POP Cornice", "file": "pop_cornice.jpg", "url": "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=150&h=150&fit=crop"},
        {"title": "Basic English WC", "file": "basic_wc.jpg", "url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=150&h=150&fit=crop"},
        {"title": "Basic Fitting Taps", "file": "basic_taps.jpg", "url": "https://images.unsplash.com/photo-1584622781564-1d987f7333c1?w=150&h=150&fit=crop"},
        {"title": "Basic Granite Slab", "file": "granite_slab.jpg", "url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=150&h=150&fit=crop"}
    ]
else: # Premium Luxury
    img_data = [
        {"title": "Designer Main Door", "file": "designer_main_door.jpg", "url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=150&h=150&fit=crop"},
        {"title": "Modular Kitchen", "file": "modular_kitchen.jpg", "url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=150&h=150&fit=crop"},
        {"title": "Designer Wardrobe", "file": "designer_wardrobe.jpg", "url": "https://images.unsplash.com/photo-1558882224-cca166733360?w=150&h=150&fit=crop"},
        {"title": "Glass Railing", "file": "glass_railing.jpg", "url": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=150&h=150&fit=crop"},
        {"title": "Wall Hung WC", "file": "wall_hung_wc.jpg", "url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?w=150&h=150&fit=crop"},
        {"title": "Premium Diverter", "file": "diverter.jpg", "url": "https://images.unsplash.com/photo-1584622781564-1d987f7333c1?w=150&h=150&fit=crop"},
        {"title": "False Ceiling", "file": "false_ceiling.jpg", "url": "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=150&h=150&fit=crop"},
        {"title": "SS Main Gate", "file": "ss_main_gate.jpg", "url": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=150&h=150&fit=crop"},
        {"title": "SS Staircase Railing", "file": "ss_staircase_railing.jpg", "url": "https://images.unsplash.com/photo-1512915922686-57c11dde9b6b?w=150&h=150&fit=crop"},
        {"title": "Live CCTV System", "file": "cctv_system.jpg", "url": "https://images.unsplash.com/photo-1557597774-9d273605dfa9?w=150&h=150&fit=crop"}
    ]

# Render Image Section with clear beautiful flex grids
for img in img_data:
    resolved_src = get_image_source(img['file'], img['url'])
    images_html += f"""
    <div style="text-align: center; width: 130px; margin: 5px; border: 1px solid #e5e7eb; border-radius: 8px; padding: 6px; background-color: #fafafa;">
        <img src="{resolved_src}" style="width: 110px; height: 95px; border-radius: 6px; object-fit: cover; border: 1px solid #d1d5db;" alt="{img['title']}">
        <div style="font-size: 11px; font-weight: 700; margin-top: 6px; color: #1f2937; line-height: 1.2;">{img['title']}</div>
    </div>"""

# 6. BRANDS ECOSYSTEM
brands_list = ["Action Tesa", "Anchor", "Astral Pipes", "Berger", "SAINIK 710", "Chivas Ply", "Greenply", "Johnson Tiles", "Kajaria", "Kamdhenu NXT", "Kangaro", "Rathi Steel", "Rathi TMT", "SAINIK DOORS", "Somany", "Varmora"]
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
        excel_specs_html += "<li><b>Scope Definition:</b> Structural Framework combined with Standard Functional Finishing.</li>"
    else:
        excel_specs_html += "<li><b>Front Elevation:</b> Modern Design Elevation Framework with dynamic lighting controls.</li>"

# 8. TABLE DATA ROWS
table_rows_html = ""
for item in floor_data:
    subtotal = item['area'] * item['rate']
    table_rows_html += f"""
    <tr style="border-bottom: 1px solid #e5e7eb;">
        <td style="padding: 10px; font-size: 13px; color: #111827; font-weight: 500;">{item['floor']}</td>
        <td style="padding: 10px; font-size: 13px; color: #2563eb; font-weight: 600;">{item['layout']}</td>
        <td style="padding: 10px; font-size: 13px; color: #4b5563; text-align: center;">{item['area']:,} Sq.Ft</td>
        <td style="padding: 10px; font-size: 13px; color: #111827; text-align: right; font-weight: 600;">Rs. {subtotal:,.2f}</td>
    </tr>"""

# 9. SAFE HTML STRING CONSTRUCT
formatted_total_cost = f"Rs. {net_project_cost:,.2f}"
formatted_built_up_str = f"{total_built_up:,} Total Built-up PSF"
formatted_plot_ref_str = f"{plot_area_yd} Yd ({plot_area_ft_ref} Sq.Ft Ref)"

proposal_html = f"""
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
            <b>Quotation Ref:</b> SBBT/Q/2026/095<br>
            <b>Client Name:</b> {client_name}<br>
            <b>Project Location:</b> {project_address}<br>
            <b>Quotation Type:</b> <span style="color:#2563eb; font-weight:700;">{selected_global_display}</span>
        </div>
        <div style="text-align: right;">
            <b>Date Issued:</b> {datetime.date.today().strftime('%d %B %Y')}<br>
            <b>Plot Frame Reference:</b> {formatted_plot_ref_str}<br>
            <b>Total Structure Config:</b> {total_floors} Floors ({formatted_built_up_str})
        </div>
    </div>

    <div style="margin-top: 15px; background-color: #fafafa; border-left: 3px solid #2563eb; padding: 12px; font-style: italic; font-size: 13px; color: #4b5563; border-radius: 0 6px 6px 0;">
        "{custom_note}"
    </div>

    <div style="margin-top: 20px; border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px; background-color: #ffffff;">
        <div style="font-weight: 700; font-size: 12px; color: #111827; margin-bottom: 12px; text-align: center; letter-spacing: 0.5px; text-transform: uppercase; border-bottom: 1px solid #eee; padding-bottom: 6px;">📸 Visual Scope Material Inclusion Details ({selected_global_display}):</div>
        <div style="display: flex; gap: 4px; justify-content: center; flex-wrap: wrap;">
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
                    <th style="padding: 10px; font-size: 13px;">Layout & Configuration</th>
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
        <div>
            <span style="font-weight: 800; font-size: 11px; color: #1e40af; letter-spacing: 0.5px; display:block; text-transform: uppercase;">PACKAGE: {selected_global_display}</span>
            <span style="font-weight: 700; font-size: 13px; color: #111827;">TOTAL CONSTRUCTION INVESTMENT (GST INC.):</span>
        </div>
        <span style="font-size: 22px; font-weight: 800; color: #1e3a8a;">{formatted_total_cost}</span>
    </div>

    <div style="margin-top: 15px; background-color: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 14px; font-size: 12px; color: #78350f;">
        <div style="font-weight: 700; font-size:13px; text-transform: uppercase; margin-bottom:4px; color: #92400e;">⚡ Commercial Terms & Proposal Validity:</div>
        • <b>Validity Note:</b> This official executive quotation is strictly <b>valid for 30 days</b> from the date of release.<br>
        • <b>Inclusions:</b> All materials specified in the technical specifications matrix correspond directly to the customized choices.
        <div style="color: #92400e; margin-top: 6px; font-weight: 600;">Additional Commitments: {additional_reqs}</div>
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

# 10. PRINT CONFIGURATION VIA IFRAME COMPATIBLE HEADERS
full_html_page = f"""<!DOCTYPE html><html><head><meta charset='utf-8'>
<style>
@media print {{
  body {{ padding: 0; background: #fff; }}
  .no-print {{ display: none !important; }}
}}
</style>
</head>
<body style='margin:0; padding:20px; background-color:#ffffff;'>
{proposal_html}
<script>
window.onload = function() {{
    setTimeout(function() {{ window.print(); }}, 500);
}};
</script>
</body></html>"""

# 11. UI INTERFACE DISPLAY
st.write("### 💎 Live Executive Proposal Preview")
st.caption("Aap niche diye gaye button par click karke direct print layout download kar sakte hain:")

st.download_button(
    label="📥 Download & Save Proposal Page",
    data=full_html_page,
    file_name=f"SBBT_Proposal_{client_name.replace(' ', '_')}.html",
    mime="text/html",
    type="primary"
)

st.write("")
st.markdown(proposal_html, unsafe_allow_html=True)
