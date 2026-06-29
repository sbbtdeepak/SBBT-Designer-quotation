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
    total_floors = st.slider("Number of Floors to Configure (e.g., G+1, G+3)", min_value=1, max_value=12, value=3)

plot_area_ft_ref = plot_area_yd * 9

st.write("---")
st.subheader("📐 Step 2: Custom Floor Layout & Area Configuration")

floor_data = []
total_built_up = 0.0

if "Solid Structure" in selected_global_display:
    def_rate_val = 1199
elif "Essential" in selected_global_display:
    def_rate_val = 1700
else:
    def_rate_val = 2300

for i in range(total_floors):
    floor_label = "Ground Floor / Stilt" if i == 0 else "First Floor" if i == 1 else "Second Floor" if i == 2 else "Third Floor" if i == 3 else f"{i}th Floor"
    
    st.markdown(f"#### 🏢 {floor_label}")
    fl_col1, fl_col2, fl_col3 = st.columns([1.5, 2.0, 1.5])
    
    with fl_col1:
        f_area = st.number_input(f"Built Area (Sq.Ft)", min_value=50, max_value=10000, value=int(plot_area_ft_ref), key=f"area_val_{i}")
    
    with fl_col2:
        f_layout = st.text_input(f"Layout Configuration", value="3 BHK with Attach Bathroom" if i > 0 else "Stilt Parking + 1 Office", key=f"layout_val_{i}")
        
    with fl_col3:
        f_rate = st.number_input(f"Rate (Rs/PSF)", min_value=500, max_value=5000, value=def_rate_val, key=f"rate_val_{i}")
        
    floor_data.append({"floor": floor_label, "area": f_area, "layout": f_layout, "rate": f_rate})
    total_built_up += f_area

# 🛠️ DYNAMIC CLIENT DEFINED ADDITIONAL WORK SCOPE
st.write("---")
st.subheader("➕ Step 3: Client Defined Additional Work Scope")

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

custom_note = st.text_area("Client Dedication Note", "We are offering a special commercial advantage for your property while maintaining premium specifications and long-term value, ensuring trust with zero compromises.")
additional_reqs = st.text_area("Extra Strategic Commitments", "Includes specialized brand structural alignments, earthquake resistant RCC frame configuration, and comprehensive support services.")

# MATHEMATICAL PROJECT TOTALS
net_project_cost = sum(item['area'] * item['rate'] for item in floor_data)
for scope in additional_scopes:
    net_project_cost += scope['cost']

# 📊 14. SMART DYNAMIC PAYMENT FRAMEWORK WITH TOGGLE LOCK
st.write("---")
st.subheader("💳 Step 4: Smart Milestone Activation Control")

# CRITICAL TOGGLE AT THE MIDDLE OF PROCESS FOR MASTER LOCKING
final_ok_switch = st.toggle("🔒 LOCK AND VERIFY MILESTONES (FINAL OK)", value=False, help="Is switch ko ON karne ke baad hi client quotation table me amounts details preview hongi.")

# Milestone Allocation Definitions
pct_booking = 6.0
pct_foundation = 10.0
pct_plinth = 6.0
pct_structure_per_floor = 8.4  # Exact User Override Constraint

# Baseline Setup
default_stages = [
    {"stage": "Booking Advance Security Split", "desc": "Initial site mobilization, machinery logistics setup, architectural structural layouts alignment and legal authorization.", "pct": pct_booking},
    {"stage": "Foundation Base Infrastructure", "desc": "Complete deep excavation work, PCC leveling layout, structural column footing mesh layout, and foundation monolithic base casting.", "pct": pct_foundation},
    {"stage": "Plinth Level Integration Framework", "desc": "Plinth Beam structural frame execution, anti-termite ground treatment, sand filling, deep compaction, and specialized DPC protective layer setups.", "pct": pct_plinth}
]

# Structure Floor Wise Generation
for i in range(total_floors):
    floor_label = "Ground Floor" if i == 0 else "First Floor" if i == 1 else "Second Floor" if i == 2 else "Third Floor" if i == 3 else f"{i}th Floor"
    default_stages.append({
        "stage": f"{floor_label} Structure & Brickwork Combined",
        "desc": f"Execution of vertical heavy RCC columns, beam alignments, roof slab grid layout casting, structural staircase installation, and complete outer/inner line brick wall masonry layouts.",
        "pct": pct_structure_per_floor
    })

default_stages.append({
    "stage": "Electrical & Plumbing In-Wall Concealed Works",
    "desc": "Chasing/jiri layout tracking in brick walls, structural placement of heavy PVC fire-retardant electrical conduits, and execution of internal pipeline water connectivity distribution lines.",
    "pct": 5.0
})

default_stages.append({
    "stage": "Floor-wise Internal & External Plaster Completion",
    "desc": "Laying of precise rich-mortar cement internal surfaces plastering and synchronized outer high-strength weather-proof external finish plaster layouts.",
    "pct": 8.0
})

# Dynamic Floor Wise Flooring Distribution
if "Solid Structure" not in selected_global_display:
    pct_flooring_pool = 12.0
    flooring_per_floor = round(pct_flooring_pool / total_floors, 2)
    for i in range(total_floors):
        floor_label = "Ground Floor" if i == 0 else "First Floor" if i == 1 else "Second Floor" if i == 2 else "Third Floor" if i == 3 else f"{i}th Floor"
        default_stages.append({
            "stage": f"{floor_label} Internal Flooring & Architectural Tiling Work",
            "desc": f"Installation of high-end vitrified tiling elements or premium granite layouts, specialized bathroom floor-to-wall tiling layouts, and kitchen counter slate setup frames.",
            "pct": flooring_per_floor
        })

    default_stages.append({"stage": "Doors, Windows Frame & Security Railings Setup", "desc": "Fixing durable perimeter frames, secure window panels setups, high-strength inner flush door leaves, and architectural steel or glass handrails.", "pct": 8.0})
    default_stages.append({"stage": "Wall Smooth Putty, Base Paint & Premium Fixtures", "desc": "Dual coat structural wall putty treatment, base primers paint coatings, fixing designer modular switches, and structural sanitary systems execution.", "pct": 7.0})

# Dynamically calculate remaining balance to maintain absolute 100% boundary
allocated_sum = sum(stg['pct'] for stg in default_stages)
pct_handover = round(max(0.0, 100.0 - allocated_sum), 2)

default_stages.append({
    "stage": "Final Custom Detailing, Deep Cleaning & Keys Handover",
    "desc": "Thorough post-project deep cleaning operations, polishing verification, dynamic validation checklist oversight, and corporate site keys handover protocol.",
    "pct": pct_handover
})

edited_stages = []
current_running_sum = 0.0

st.markdown("#### ✏️ Administrative Stage Percentage Overrides Controls")
for idx, stg in enumerate(default_stages):
    st_col1, st_col2 = st.columns([3.6, 1.4])
    with st_col1:
        st.markdown(f"**Stage {idx+1}:** {stg['stage']}  \n*{stg['desc']}*")
    with st_col2:
        val_override = st.number_input("Stage % Allocation", min_value=0.0, max_value=100.0, value=float(stg['pct']), step=0.01, key=f"stg_override_pct_{idx}")
        edited_stages.append({"stage": stg['stage'], "desc": stg['desc'], "pct": val_override})
        current_running_sum += val_override

current_running_sum = round(current_running_sum, 2)
if current_running_sum != 100.0 and len(edited_stages) > 0:
    difference_offset = round(100.0 - current_running_sum, 2)
    edited_stages[-1]['pct'] = round(edited_stages[-1]['pct'] + difference_offset, 2)
    current_running_sum = 100.0

st.success("✅ Dynamic payment percentages synchronized seamlessly to 100.00% standard framework configuration!")

# GENERATE HTML PREVIEW BLOCKS BASED ON TOGGLE STATE
payment_schedule_rows = ""
for idx, milestone in enumerate(edited_stages):
    stage_calculated_cost = (milestone['pct'] / 100.0) * net_project_cost
    
    # Hide details if switch is OFF
    if final_ok_switch:
        pct_display = f"{milestone['pct']:.2f}%"
        cost_display = f"Rs. {stage_calculated_cost:,.2f}"
    else:
        pct_display = "🔒 Locked"
        cost_display = "🔒 Pending Master Approval"
        
    payment_schedule_rows += f"""
    <tr style="border-bottom: 1px solid #e5e7eb;">
        <td style="padding: 10px; font-size: 12.5px; color: #111827; font-weight: 700; background-color: #fafafa; text-align: center;">{idx+1}</td>
        <td style="padding: 10px; font-size: 13px; color: #111827; font-weight: 700;">{milestone['stage']}</td>
        <td style="padding: 10px; font-size: 12px; color: #4b5563; line-height:1.4;">{milestone['desc']}</td>
        <td style="padding: 10px; font-size: 13px; color: #2563eb; font-weight: 800; text-align: center; background-color: #f0fdf4;">{pct_display}</td>
        <td style="padding: 10px; font-size: 13px; color: #111827; font-weight: 800; text-align: right;">{cost_display}</td>
    </tr>"""

# DYNAMIC IMAGE ASSIGNMENT LOGIC
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
        {"title": "Flush Door", "file": "flush_door.jpg", "url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=150&h=150&fit=crop"}
    ]
else: # Premium Luxury
    img_data = [
        {"title": "🏛️ HPL Cladding Elevation", "file": "hpl_cladding.jpg", "url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=150&h=150&fit=crop"},
        {"title": "Designer Main Door", "file": "designer_main_door.jpg", "url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?w=150&h=150&fit=crop"},
        {"title": "Modular Kitchen", "file": "modular_kitchen.jpg", "url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=150&h=150&fit=crop"},
        {"title": "Designer Wardrobe", "file": "designer_wardrobe.jpg", "url": "https://images.unsplash.com/photo-1558882224-cca166733360?w=150&h=150&fit=crop"}
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

# DYNAMIC BRAND LOGO RENDERING MATRIX
brands_data = [
    {"name": "TATA Steel", "icon": "⛓️"}, {"name": "JINDAL Steel", "icon": "🏗️"},
    {"name": "UltraTech Cement", "icon": "🧱"}, {"name": "Ambuja Cement", "icon": "🦅"},
    {"name": "Kajaria Tiles", "icon": "💎"}, {"name": "Astral Pipes", "icon": "🚰"},
    {"name": "Berger Paints", "icon": "🎨"}, {"name": "Greenply", "icon": "🌳"}
]

brands_html = ""
for brand in brands_data:
    brands_html += f"""
    <div style="display: flex; align-items: center; gap: 6px; background: #ffffff; border: 1px solid #e5e7eb; border-radius: 6px; padding: 6px 12px; min-width: 145px; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
        <span style="font-size: 16px;">{brand['icon']}</span>
        <span style="font-size: 11px; font-weight: 700; color: #111827;">{brand['name']}</span>
    </div>"""

# SPECIFICATION LIST BUILDER
excel_specs_html = ""
if df_matrix is not None and selected_excel_col in df_matrix.columns:
    for idx, row in df_matrix.iterrows():
        cat = row['Category / Element'] if 'Category / Element' in df_matrix.columns else row.iloc[0]
        spec = row[selected_excel_col]
        if pd.notna(spec) and "Excluded" not in str(spec):
            excel_specs_html += f"<li style='margin-bottom:6px;'><b>{cat}:</b> {spec}</li>"
else:
    specs_list = [
        ("Structural Framework Elements", "M25 Premium Grade machine concrete core with strict engineering slump slump verification."),
        ("Steel & Core Reinforcement", "Exclusively TATA Tiscon / JINDAL Panther high-tensile structural TMT Fe-550D steel layouts."),
        ("Cement Infrastructure Base", "UltraTech Premium / Ambuja Kawach specialized high-strength weather-proof grade binders."),
        ("Waterproofing Protocol Systems", "Multi-layered advanced dynamic chemical waterproofing across all sunken regions and terrace fields.")
    ]
    for cat, spec in specs_list:
        excel_specs_html += f"<li style='margin-bottom:7px;'><b>{cat}:</b> {spec}</li>"

# GENERAL BREAKDOWN TABLE DATA GENERATION
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

for scope in additional_scopes:
    table_rows_html += f"""
    <tr style="border-bottom: 1px solid #e5e7eb; background-color: #f8fafc;">
        <td style="padding: 12px; font-size: 13px; color: #0f172a; font-weight: 700; background-color: #f1f5f9;">➕ Add-on Scope</td>
        <td style="padding: 12px; font-size: 13px; color: #0284c7; font-weight: 700;">✨ {scope['name']}</td>
        <td style="padding: 12px; font-size: 13px; color: #64748b; text-align: center;">1 Job</td>
        <td style="padding: 12px; font-size: 13px; color: #64748b; text-align: center;">Custom Lumpsum</td>
        <td style="padding: 12px; font-size: 13px; color: #0f172a; text-align: right; font-weight: 700;">Rs. {scope['cost']:,.2f}</td>
    </tr>"""

formatted_total_cost = f"Rs. {net_project_cost:,.2f}"
formatted_plot_ref_str = f"{plot_area_yd} Sq. Yards ({plot_area_ft_ref} Sq.Ft Reference Frame)"

# PRESENTATION GENERATOR ASSEMBLY
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

        <div style="margin-top: 25px; background-color: #f0fdf4; border-left: 4px solid #16a34a; padding: 15px; font-style: italic; font-size: 13.5px; color: #14532d; border-radius: 0 8px 8px 0;">
            <b>Director's Note:</b> {custom_note}
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
                <span style="font-size: 11px; color: #9ca3af; font-weight: 700; display: block; text-transform: uppercase;">Aggregated Commercial Valuation Matrix</span>
                <span style="font-size: 12px; color: #38bdf8; font-weight: 700;">Includes structural machinery, material supplies, and execution components.</span>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 22px; font-weight: 800; color: #38bdf8;">{formatted_total_cost}</span>
                <span style="font-size: 11px; display: block; color: #9ca3af;">Net Complete Investment Framework</span>
            </div>
        </div>
    </div>

    <div style="border: 1px solid #d1d5db; border-radius: 12px; padding: 35px; background: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.02); margin-bottom: 30px; page-break-after: always;">
        <h3 style="font-size: 14px; font-weight: 800; color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 0;">💳 2. Smart Auto-Generated Stage Billing Milestone Matrix</h3>
        <p style="font-size: 12px; color: #4b5563; margin-top: 6px; margin-bottom: 15px;">The construction payouts are strictly calibrated in structured progress cycles matching structural or finishing dependencies safely:</p>
        
        <table style="width: 100%; border-collapse: collapse; text-align: left; margin-top: 10px;">
            <thead>
                <tr style="background-color: #1f2937; color: #ffffff;">
                    <th style="padding: 10px; font-size: 11.5px; text-transform: uppercase; text-align: center; width: 40px;">S.No</th>
                    <th style="padding: 10px; font-size: 11.5px; text-transform: uppercase; width: 230px;">Milestone Stage</th>
                    <th style="padding: 10px; font-size: 11.5px; text-transform: uppercase;">Detailed Technical Work Definition Scope</th>
                    <th style="padding: 10px; font-size: 11.5px; text-transform: uppercase; text-align: center; width: 80px;">Stage %</th>
                    <th style="padding: 10px; font-size: 11.5px; text-transform: uppercase; text-align: right; width: 140px;">Due Amount (INR)</th>
                </tr>
            </thead>
            <tbody>
                {payment_schedule_rows}
            </tbody>
        </table>
        
        <div style="margin-top: 25px; background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; font-size: 12px; line-height: 1.5; color: #334155;">
            <b style="color: #0f172a; text-transform: uppercase; display: block; margin-bottom: 5px;">⚡ Core Structural Compliance & Quality Assurances</b>
            • All structural monolithic concrete pours will undergo strict cube sampling tests verified via independent NABL laboratory protocols.<br>
            • Steel supplies are directly sourced from primary producers ensuring raw material certification tracking against rust or batch anomalies.<br>
            • Any client-requested alterations inside layout spaces after structural casting milestones are initiated will attract distinct job sheets variation costs.
        </div>
    </div>

    <div style="border: 1px solid #d1d5db; border-radius: 12px; padding: 35px; background: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
        <h3 style="font-size: 14px; font-weight: 800; color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 0;">📸 3. Visual Scope Material Inclusion Details</h3>
        <div style="display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; background: #fafafa; padding: 12px; border-radius: 8px; border: 1px solid #e5e7eb; margin-top:10px;">
            {images_html}
        </div>

        <h3 style="font-size: 14px; font-weight: 800; color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 25px;">🏢 4. Strategic Brand Tie-Ups</h3>
        <div style="display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; background: #fafafa; padding: 12px; border-radius: 8px; border: 1px solid #e5e7eb; margin-top:10px;">
            {brands_html}
        </div>

        <h3 style="font-size: 14px; font-weight: 800; color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 25px;">🛠️ 5. Technical Specifications & Material Directives</h3>
        <ul style="padding-left: 18px; font-size: 12.5px; color: #374151; line-height: 1.6; margin-top: 10px;">
            {excel_specs_html}
        </ul>

        <h3 style="font-size: 14px; font-weight: 800; color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 25px;">🛡️ 6. Commercial Execution Terms & Guarantees</h3>
        <div style="background-color: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 14px; font-size: 12.5px; color: #78350f; line-height: 1.6; margin-top: 10px;">
            • <b>Commercial Validity:</b> This document valuation parameters stand legally locked for 30 days from layout logging.<br>
            • <b>Quality Controls:</b> Execution parameters tracked via comprehensive **100+ points system checklist** checks.<br>
            • <b>Strategic Accords:</b> {additional_reqs}
        </div>

        <h3 style="font-size: 14px; font-weight: 800; color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 25px;">⏱️ 7. Payment Frequency & Clearing Protocols</h3>
        <div style="background-color: #f0fdfa; border: 1px solid #99f6e4; border-radius: 8px; padding: 14px; font-size: 12.5px; color: #115e59; line-height: 1.6; margin-top: 10px;">
            • <b>Invoice Generation Frequency:</b> Invoices will be raised strictly upon the formal 100% completion of each designated milestone stage listed in Section 2.<br>
            • <b>Verification Window:</b> Client is granted a 72-hour window post stage completion to audit site progress before payment release operations.<br>
            • <b>Clearing TAT:</b> All milestone payments must be credited via Bank Transfer (RTGS/NEFT) within 4 working days of invoice tracking to avoid logistical deployment halts.
        </div>

        <div style="margin-top: 40px; border-top: 2px solid #111827; padding-top: 20px; display: flex; justify-content: space-between; align-items: end; font-size: 12px; color: #4b5563;">
            <div>
                <br><br><br>
                <span style="font-size: 11px; color: #9ca3af; font-style: italic; display:block; margin-bottom:2px;">Signature of Executive Authority</span>
                <b>Shree Badree Build Tech Pvt. Ltd.</b>
            </div>
            <div style="text-align: right; line-height: 1.5; font-size: 12px; color: #111827;">
                🏢 <b>Head Office:</b> New Delhi, NCR, India<br>
                📞 <b>Contact Desk:</b> +91 8800614403, 9625803339<br>
                🌐 <b>Digital Identity:</b> <a href="https://sbbt.in" style="color: #2563eb; text-decoration: none; font-weight: 700;">sbbt.in</a>
            </div>
        </div>
    </div>

</div>
"""

# PRINT INCLUSION MATRIX
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

# SCREEN RENDERING PIPELINE
st.write("### 💎 Live Executive Proposal Preview")
st.caption("Niche diye gaye component ke dwara live breakdown check karein ya print out page download karein:")

st.download_button(
    label="📥 Download & Save Proposal Page",
    data=full_html_page,
    file_name=f"SBBT_Proposal_{client_name.replace(' ', '_')}.html",
    mime="text/html",
    type="primary"
)

st.write("")
st.markdown(proposal_html, unsafe_allow_html=True)
