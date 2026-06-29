import streamlit as st
import pandas as pd
import datetime
import os

# 1. PAGE SETUP & THEME
st.set_page_config(page_title="SBBT Executive Proposal Engine", page_icon="🏗️", layout="centered")

# IMAGE CONFIGURATION HELPER
def get_image_source(file_name, fallback_url):
    github_username = "sbbtdeepak"  
    github_repo = "SBBT-Designer-quotation"  
    return f"https://raw.githubusercontent.com/{github_username}/{github_repo}/main/images/{file_name}"

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
st.subheader("📐 Step 2: Custom Floor Layout & Area Configuration")

floor_data = []
total_built_up = 0.0

for i in range(total_floors):
    floor_label = "Ground Floor / Stilt" if i == 0 else "First Floor" if i == 1 else "Second Floor" if i == 2 else "Third Floor" if i == 3 else f"{i}th Floor"
    
    st.markdown(f"#### 🏢 {floor_label}")
    fl_col1, fl_col2, fl_col3 = st.columns([1.5, 2.0, 1.5])
    
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
        f_rate = st.number_input(f"Rate (Rs/PSF)", min_value=min_p, max_value=max_p, value=def_p, key=f"rate_val_{i}")
        
    floor_data.append({"floor": floor_label, "area": f_area, "layout": f_layout, "rate": f_rate})
    total_built_up += f_area

# 🛠️ UPDATED FEATURE: 100% DYNAMIC CLIENT DEFINED ADDITIONAL WORK SCOPE
st.write("---")
st.subheader("➕ Step 3: Client Defined Additional Work Scope")
st.caption("Client ki requirement ke mutabik scope ka naam aur cost yahan daalein. Toggle ON hone par hi table me dikhega.")

additional_scopes = []

for idx in range(3):
    st.markdown(f"**Custom Scope Item {idx+1}**")
    sc_col1, sc_col2, sc_col3 = st.columns([1.2, 2.3, 1.5])
    
    with sc_col1:
        toggle_active = st.toggle(f"Enable Item {idx+1}", value=False, key=f"tg_active_{idx}")
    
    with sc_col2:
        scope_name = st.text_input(f"Scope / Work Name", placeholder="e.g., Heavy Elevator / Boundary Wall", key=f"sc_name_{idx}", disabled=not toggle_active)
    
    with sc_col3:
        scope_cost = st.number_input(f"Lumpsum Cost (Rs.)", min_value=0, value=0, step=5000, key=f"sc_cost_{idx}", disabled=not toggle_active)
        
    if toggle_active and scope_name.strip():
        additional_scopes.append({"name": scope_name.strip(), "cost": scope_cost})

st.write("---")
custom_note = st.text_area("Client Dedication Note", "We are offering a special commercial advantage for your property while maintaining premium specifications and long-term value, ensuring trust with zero compromises.")
additional_reqs = st.text_area("Extra Strategic Commitments", "Includes specialized brand structural alignments, earthquake resistant RCC frame configuration, and comprehensive support services.")

# MATHEMATICAL COMPUTATION (DYNAMIC INTEGRATION)
net_project_cost = sum(item['area'] * item['rate'] for item in floor_data)
for scope in additional_scopes:
    net_project_cost += scope['cost']

# 5. DYNAMIC IMAGE ASSIGNMENT LOGIC
images_html = ""
if "Solid Structure" in selected_global_display:
    img_data = [
        {"title": "📐 Plain Elevation", "file": "plain_elevation.jpg", "url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=150&h=150&fit=crop"},
        {"title": "RCC Core Frame", "file": "rcc_frame.jpg", "url": "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=150&h=150&fit=crop"},
        {"title": "Robust Brickwork", "file": "brickwork.jpg", "url": "https://images.unsplash.com/photo-1590069261209-f8e9b8642343?w=150&h=150&fit=crop"},
        {"title": "Plaster Completed", "file": "plaster.jpg", "url": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?w=150&h=150&fit=crop"}
    ]
elif "Essential" in selected_global_display:
    img_data = [
        {"title": "🏙️ ACP Elevation", "file": "acp_elevation.jpg", "url": "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?w=150&h=150&fit=crop"},
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
        {"title": "🏛️ HPL Cladding Elevation", "file": "hpl_cladding.jpg", "url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=150&h=150&fit=crop"},
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

for img in img_data:
    resolved_src = get_image_source(img['file'], img['url'])
    is_elevation = "Elevation" in img['title'] or "Cladding" in img['title']
    bg_color = "#eff6ff" if is_elevation else "#ffffff"
    border_color = "#2563eb" if is_elevation else "#e5e7eb"
    
    images_html += f"""
    <div style="text-align: center; width: 125px; margin: 6px; border: 1px solid {border_color}; border-radius: 8px; padding: 6px; background-color: {bg_color}; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
        <img src="{resolved_src}" style="width: 110px; height: 90px; border-radius: 5px; object-fit: cover;" alt="{img['title']}" onerror="this.onerror=null; this.src='{img['url']}';">
        <div style="font-size: 11px; font-weight: 700; margin-top: 6px; color: #111827; line-height: 1.2;">{img['title']}</div>
    </div>"""

# 6. DYNAMIC BRAND LOGO RENDERING MATRIX
brands_data = [
    {"name": "TATA Steel", "icon": "⛓️"}, {"name": "JINDAL Steel", "icon": "🏗️"},
    {"name": "UltraTech Cement", "icon": "🧱"}, {"name": "Ambuja Cement", "icon": "🦅"},
    {"name": "ACC Cement", "icon": "💪"}, {"name": "Kajaria Tiles", "icon": "💎"},
    {"name": "Action Tesa", "icon": "🪵"}, {"name": "Astral Pipes", "icon": "🚰"},
    {"name": "Berger Paints", "icon": "🎨"}, {"name": "SAINIK 710 Ply", "icon": "🪓"},
    {"name": "Greenply", "icon": "🌳"}, {"name": "Johnson Tiles", "icon": "🧱"},
    {"name": "Anchor Panasonic", "icon": "🔌"}, {"name": "Somany Tiles", "icon": "✨"}
]

brands_html = ""
for brand in brands_data:
    brands_html += f"""
    <div style="display: flex; align-items: center; gap: 6px; background: #ffffff; border: 1px solid #e5e7eb; border-radius: 6px; padding: 6px 12px; min-width: 145px; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
        <span style="font-size: 16px;">{brand['icon']}</span>
        <span style="font-size: 11px; font-weight: 700; color: #111827;">{brand['name']}</span>
    </div>"""

# 7. SPECIFICATION LIST BUILDER
excel_specs_html = ""
if df_matrix is not None and selected_excel_col in df_matrix.columns:
    for idx, row in df_matrix.iterrows():
        cat = row['Category / Element'] if 'Category / Element' in df_matrix.columns else row.iloc[0]
        spec = row[selected_excel_col]
        if pd.notna(spec) and "Excluded" not in str(spec):
            excel_specs_html += f"<li style='margin-bottom:6px;'><b>{cat}:</b> {spec}</li>"
else:
    elevation_text = "Plain Textured Render / Classic Paint Finish Elevation Layout." if "Solid Structure" in selected_global_display else "Premium Weather-Proof Aluminium Composite Panel (ACP) Grid Elevation Configuration." if "Essential" in selected_global_display else "Ultra-Luxury High-Pressure Laminate (HPL) Cladding mixed with Toughened Architectural Glass Profile."
    specs_list = [
        ("Front Elevation Facade", elevation_text),
        ("Structural Framework", "M25 Premium Grade heavy-duty machine concrete core with strict slump verification protocols."),
        ("Steel & Core Reinforcement", "Exclusively TATA Tiscon / JINDAL Panther high-tensile structural TMT Fe-550D steel layouts."),
        ("Cement Infrastructure", "UltraTech Premium / Ambuja Kawach specialized weather-proof grade block casting & masonry binders."),
        ("Masonry & Brickwork", "Premium Grade red clay bricks / high-strength autoclaved blocks cured dynamically."),
        ("Plumbing & Drainage Network", "Concealed CPVC/UPVC architectural pipeline layouts via Astral or Finolex systems."),
        ("Electrical Infrastructure", "Concealed heavy-duty fire-retardant wiring layouts using Polycab / Havells with modern sleek modular switch configurations."),
        ("Premium Wall & Floor Finishes", "Vitrified large-format tiles (600x600mm / 800x800mm) by Kajaria, Somany, or Johnson tiles."),
        ("Waterproofing Protocol", "Multi-layered advanced dynamic chemical waterproofing across all sunken regions, bathrooms, and open terrace fields.")
    ]
    for cat, spec in specs_list:
        excel_specs_html += f"<li style='margin-bottom:7px;'><b>{cat}:</b> {spec}</li>"

# 8. FLOOR ROWS & CUSTOM SCOPES (VISIBLE ONLY IF ACTIVE)
table_rows_html = ""
for item in floor_data:
    subtotal = item['area'] * item['rate']
    table_rows_html += f"""
    <tr style="border-bottom: 1px solid #e5e7eb;">
        <td style="padding: 12px; font-size: 13px; color: #111827; font-weight: 600; background-color: #fafafa;">{item['floor']}</td>
        <td style="padding: 12px; font-size: 13px; color: #2563eb; font-weight: 700;">{item['layout']}</td>
        <td style="padding: 12px; font-size: 13px; color: #4b5563; text-align: center;">{item['area']:,} Sq.Ft</td>
        <td style="padding: 12px; font-size: 13px; color: #4b5563; text-align: center; font-weight: 600;">Rs. {item['rate']:,} / PSF</td>
        <td style="padding: 12px; font-size: 13px; color: #111827; text-align: right; font-weight: 700;">Rs. {subtotal:,.2f}</td>
    </tr>"""

# APPENDING USER CUSTOM CLIENT DEFINED SCOPES
for scope in additional_scopes:
    table_rows_html += f"""
    <tr style="border-bottom: 1px solid #e5e7eb; background-color: #f8fafc;">
        <td style="padding: 12px; font-size: 13px; color: #0f172a; font-weight: 700; background-color: #f1f5f9;">➕ Add-on Scope</td>
        <td style="padding: 12px; font-size: 13px; color: #0284c7; font-weight: 700;">✨ {scope['name']}</td>
        <td style="padding: 12px; font-size: 13px; color: #64748b; text-align: center;">1 Job</td>
        <td style="padding: 12px; font-size: 13px; color: #64748b; text-align: center;">Custom Lumpsum</td>
        <td style="padding: 12px; font-size: 13px; color: #0f172a; text-align: right; font-weight: 700;">Rs. {scope['cost']:,.2f}</td>
    </tr>"""

# 9. MULTI-PAGE STRUCTURED PROPOSAL DESIGN
formatted_total_cost = f"Rs. {net_project_cost:,.2f}"
formatted_plot_ref_str = f"{plot_area_yd} Sq. Yards ({plot_area_ft_ref} Sq.Ft Reference Frame)"

proposal_html = f"""
<div style="background-color: #ffffff; color: #111827; font-family: 'Segoe UI', Arial, sans-serif; max-width: 850px; margin: 0 auto; padding: 10px;">
    
    <div style="border: 1px solid #d1d5db; border-radius: 12px; padding: 35px; background: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.02); margin-bottom: 30px; page-break-after: always;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #111827; padding-bottom: 20px;">
            <div>
                <h1 style="margin: 0; color: #111827; font-size: 24px; font-weight: 800; letter-spacing: 0.5px;">SHREE BADREE BUILD TECH PVT. LTD.</h1>
                <div style="font-size: 11px; color: #4b5563; font-weight: 700; margin-top: 4px; letter-spacing: 1px;">AN ISO 9001:2015 CERTIFIED CONSTRUCTION COMPANY</div>
            </div>
            <div style="text-align: right; background-color: #eff6ff; border: 1px solid #bfdbfe; padding: 8px 14px; border-radius: 8px;">
                <span style="font-size: 12px; font-weight: 800; color: #1e40af;">⭐ Google Rating: 4.9/5.0</span>
            </div>
        </div>

        <div style="margin-top: 25px; background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; font-size: 13px;">
            <div>
                <span style="color:#6b7280; font-weight:700; text-transform:uppercase; font-size:10px; display:block; margin-bottom:4px;">Prepared For:</span>
                <b>Client Name:</b> {client_name}<br>
                <b>Site Location:</b> {project_address}<br>
                <b>Proposal Framework:</b> <span style="color:#2563eb; font-weight:800;">{selected_global_display}</span>
            </div>
            <div style="text-align: right;">
                <span style="color:#6b7280; font-weight:700; text-transform:uppercase; font-size:10px; display:block; margin-bottom:4px;">Document Control:</span>
                <b>Quotation Index No:</b> SBBT/Q/2026/O95<br>
                <b>Date of Generation:</b> {datetime.date.today().strftime('%d %B %Y')}<br>
                <b>Architectural Metric:</b> {formatted_plot_ref_str}
            </div>
        </div>

        <div style="margin-top: 25px; background-color: #f0fdf4; border-left: 4px solid #16a34a; padding: 15px; font-style: italic; font-size: 13.5px; color: #14532d; border-radius: 0 8px 8px 0; line-height: 1.5;">
            "<b>Director's Note:</b> {custom_note}"
        </div>

        <div style="margin-top: 30px;">
            <h3 style="font-size: 14px; font-weight: 800; color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">📋 1. Architectural & Additional Structural Matrix</h3>
            <table style="width: 100%; border-collapse: collapse; text-align: left; margin-top: 12px;">
                <thead>
                    <tr style="background-color: #111827; color: #ffffff;">
                        <th style="padding: 12px; font-size: 12px; text-transform: uppercase;">Floor / Scope</th>
                        <th style="padding: 12px; font-size: 12px; text-transform: uppercase;">Configuration & Details</th>
                        <th style="padding: 12px; font-size: 12px; text-transform: uppercase; text-align: center;">Quantity / Area</th>
                        <th style="padding: 12px; font-size: 12px; text-transform: uppercase; text-align: center;">Unit PSF Rate</th>
                        <th style="padding: 12px; font-size: 12px; text-transform: uppercase; text-align: right;">Subtotal (INR)</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows_html}
                </tbody>
            </table>
        </div>

        <div style="margin-top: 25px; background-color: #111827; border-radius: 8px; padding: 18px; display: flex; justify-content: space-between; align-items: center; color: #ffffff;">
            <div>
                <span style="font-size: 11px; color: #9ca3af; font-weight: 700; display: block; text-transform: uppercase; letter-spacing: 0.5px;">Aggregated Investment Framework ({total_floors} Floors + Custom Client Add-ons)</span>
                <span style="font-size: 12px; color: #38bdf8; font-weight: 700;">Includes All Structural Framework, Machineries, Material Inclusions & Supervision Elements.</span>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 22px; font-weight: 800; color: #38bdf8;">{formatted_total_cost}</span>
                <span style="font-size: 11px; display: block; color: #9ca3af;">Net Investment (Inclusive of GST)</span>
            </div>
        </div>
    </div>

    <div style="border: 1px solid #d1d5db; border-radius: 12px; padding: 35px; background: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.02); margin-bottom: 30px; page-break-after: always;">
        <h3 style="font-size: 14px; font-weight: 800; color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 0;">📸 2. Visual Scope Material Inclusion Details</h3>
        <p style="font-size: 12px; color: #4b5563; margin-top: 6px; margin-bottom: 15px;">Following premium architectural finishing units stand included strictly within the customized contract outline framework:</p>
        
        <div style="display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; background: #fafafa; padding: 15px; border-radius: 8px; border: 1px solid #e5e7eb;">
            {images_html}
        </div>

        <h3 style="font-size: 14px; font-weight: 800; color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 30px;">🤝 3. Associated Corporate Material Ecosystem Brands</h3>
        <p style="font-size: 12px; color: #4b5563; margin-top: 6px; margin-bottom: 15px;">We drive your luxury structure utilizing authentic supplies procured straight from India's benchmark production houses:</p>
        
        <div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: start; background: #ffffff; border: 1px dashed #cbd5e1; padding: 20px; border-radius: 8px;">
            {brands_html}
        </div>
    </div>

    <div style="border: 1px solid #d1d5db; border-radius: 12px; padding: 35px; background: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.02);;">
        <h3 style="font-size: 14px; font-weight: 800; color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 0;">🛠️ 4. Technical Specifications & Material Directives</h3>
        <ul style="padding-left: 18px; font-size: 12.5px; color: #374151; line-height: 1.6; margin-top: 12px;">
            {excel_specs_html}
        </ul>

        <h3 style="font-size: 14px; font-weight: 800; color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 30px;">🛡️ 5. Commercial Execution Terms & Guarantees</h3>
        <div style="background-color: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 16px; font-size: 12.5px; color: #78350f; line-height: 1.6;">
            • <b>Commercial Scope Validity:</b> This estimation ledger remains legally locked and **valid for exactly 30 days** from signature date.<br>
            • <b>Quality Controls:</b> Execution monitored via comprehensive **100+ point systematic checklists** handled daily by the resident engineering desk.<br>
            • <b>Site Monitoring Provision:</b> Live 24x7 infrastructure camera lines deployed post initial earthwork to enable client transparent verification.<br>
            • <b>Strategic Accords:</b> {additional_reqs}
        </div>

        <div style="margin-top: 45px; border-top: 2px solid #111827; padding-top: 20px; display: flex; justify-content: space-between; align-items: end; font-size: 12px; color: #4b5563;">
            <div>
                <br><br><br>
                <span style="font-size: 11px; color: #9ca3af; font-style: italic; display:block; margin-bottom:2px;">Signature of Executive Authority</span>
                <b>Shree Badree Build Tech Pvt. Ltd.</b>
            </div>
            <div style="text-align: right; line-height: 1.5; font-size: 12px; color: #111827;">
                🏢 <b>Head Office:</b> New Delhi, NCR, India<br>
                📞 <b>Contact Desk:</b> +91 8800614403, 9625803339<br>
                📧 <b>Corporate Mail:</b> deeep1sharma@gmail.com<br>
                🌐 <b>Digital Identity:</b> <a href="https://sbbt.in" style="color: #2563eb; text-decoration: none; font-weight: 700;">sbbt.in</a>
            </div>
        </div>
    </div>

</div>
"""

# 10. PRINT CONFIGURATION COMPONENT
full_html_page = f"""<!DOCTYPE html><html><head><meta charset='utf-8'>
<style>
@media print {{
  body {{ padding: 0; background: #fff; }}
  .no-print {{ display: none !important; }}
  div {{ page-break-inside: avoid; }}
}}
</style>
</head>
<body style='margin:0; padding:15px; background-color:#ffffff;'>
{proposal_html}
<script>
window.onload = function() {{
    setTimeout(function() {{ window.print(); }}, 500);
}};
</script>
</body></html>"""

# 11. UI INTERFACE DISPLAY
st.write("### 💎 Live Executive Proposal Preview")
st.caption("Aap niche diye gaye button par click karke direct formal multiple-page layout download kar sakte hain:")

st.download_button(
    label="📥 Download & Save Proposal Page",
    data=full_html_page,
    file_name=f"SBBT_Proposal_{client_name.replace(' ', '_')}.html",
    mime="text/html",
    type="primary"
)

st.write("")
st.markdown(proposal_html, unsafe_allow_html=True)
