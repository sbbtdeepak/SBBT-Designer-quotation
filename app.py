import streamlit as st
import pandas as pd
import datetime
import os

# 1. PAGE SETUP & THEME
st.set_page_config(page_title="SBBT Executive Proposal Engine", page_icon="🏗️", layout="centered")

# IMAGE CONFIGURATION HELPER (Strict Single .jpg Extension from GitHub Repository)
def get_image_source(file_name):
    github_username = "sbbtdeepak"  
    github_repo = "SBBT-Designer-quotation"  
    return f"https://raw.githubusercontent.com/{github_username}/{github_repo}/main/images/{file_name}"

# 2. AUTOMATIC MATRIX LOADER
@st.cache_data
def load_sbbt_matrix():

    file_name="SBBT_Master_Quotation_Matrix.xlsx"

    try:

        if not os.path.exists(file_name):
            st.error(f"❌ File not found: {file_name}")
            return None

        xl=pd.ExcelFile(file_name)

        sheet_target="AI Master Matrix"

        if sheet_target not in xl.sheet_names:
            sheet_target=xl.sheet_names[0]

        # Detect header automatically
        raw_df = pd.read_excel(
            file_name,
            sheet_name=sheet_target,
            header=None
        )

        header_row=None

        for i,row in raw_df.iterrows():

            row_values=row.astype(str).str.strip().tolist()

            if "Category / Element" in row_values:
                header_row=i
                break

        if header_row is None:
            st.error("❌ 'Category / Element' header not found")
            return None

        # Reload with detected header
        df=pd.read_excel(
            file_name,
            sheet_name=sheet_target,
            header=header_row
        )

        df=df.dropna(how="all")

        df.columns=(
            df.columns
            .astype(str)
            .str.strip()
        )

        st.success("✅ Matrix loaded")

        return df

    except Exception as e:

        st.error(f"Excel Error: {e}")

        return None


df_matrix=load_sbbt_matrix() 
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
    plot_area_yd = st.number_input("Plot Area Reference (Sq. Yards)", min_value=10, max_value=2000, value=100)
    total_floors = st.slider("Number of Floors to Configure", min_value=1, max_value=12, value=4)

plot_area_ft_ref = plot_area_yd * 9

st.write("---")
st.subheader("📐 Step 2: Custom Floor Layout & Area Configuration")

floor_data = []
total_built_up = 0.0

if "Solid Structure" in selected_global_display:
    def_rate_val = 1200
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

# 🛠️ ADDITIONAL SCOPE
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

# INPUT WIDGETS DEFINITION
custom_note_text = st.text_area("Client Dedication Note", "We are offering a special commercial advantage for your property while maintaining premium specifications and long-term value, ensuring trust with zero compromises.")
additional_reqs_text = st.text_area("Extra Strategic Commitments", "Includes specialized brand structural alignments, earthquake resistant RCC frame configuration, and comprehensive support services.")

# MATHEMATICAL PROJECT TOTALS
net_project_cost = sum(item['area'] * item['rate'] for item in floor_data)
for scope in additional_scopes:
    net_project_cost += scope['cost']

# 📊 PAYMENT CONTROL (ON = FULL SHOW, OFF = FULL GAYAB)
st.write("---")
st.subheader("💳 Step 4: Smart Milestone Activation Control")
final_ok_switch = st.toggle("🔒 SHOW MILESTONE PAYMENT MATRIX ON PROPOSAL", value=True, help="Agar ye OFF hoga to final proposal se milestone table poori tarah gayab ho jayegi.")

# Pure Milestone Pipeline Selection
default_stages = []
if "Solid Structure" in selected_global_display:
    pct_structure_per_floor = 8.4
    total_structure_pct = pct_structure_per_floor * total_floors
    remaining_pool = 100.0 - total_structure_pct
    pct_booking = round(remaining_pool * 0.28, 2)
    pct_foundation = round(remaining_pool * 0.44, 2)
    pct_plinth = round(100.0 - total_structure_pct - pct_booking - pct_foundation, 2)
    
    default_stages.append({"stage": "Booking Advance Security Split", "desc": "Initial site mobilization, machinery logistics setup, architectural structural layouts layout and authorization.", "pct": pct_booking})
    default_stages.append({"stage": "Foundation Base Infrastructure", "desc": "Complete excavation work, PCC layout, footing column mesh layout and base casting.", "pct": pct_foundation})
    default_stages.append({"stage": "Plinth Level Integration Framework", "desc": "Plinth Beam frame execution, anti-termite treatment, compaction, and DPC protective layers.", "pct": pct_plinth})
    
    for i in range(total_floors):
        floor_label = "Ground Floor" if i == 0 else "First Floor" if i == 1 else "Second Floor" if i == 2 else "Third Floor" if i == 3 else f"{i}th Floor"
        default_stages.append({"stage": f"{floor_label} Structure & Brickwork Combined", "desc": f"RCC columns, beams alignment, slab casting and inner/outer brick wall construction.", "pct": pct_structure_per_floor})
else:
    pct_booking = 6.0
    pct_foundation = 10.0
    pct_plinth = 6.0
    pct_structure_per_floor = 6.5
    
    default_stages.append({"stage": "Booking Advance Security Split", "desc": "Initial site mobilization, architectural engineering layout and clearance maps structural framework.", "pct": pct_booking})
    default_stages.append({"stage": "Foundation Base Infrastructure", "desc": "Deep core soil excavation, mass PCC layer, monolithic footing matrix layout casting.", "pct": pct_foundation})
    default_stages.append({"stage": "Plinth Level Integration Framework", "desc": "Plinth beams grid casting, chemical anti-termite ground infusion treatment, double compact fill.", "pct": pct_plinth})
    
    for i in range(total_floors):
        floor_label = "Ground Floor" if i == 0 else "First Floor" if i == 1 else "Second Floor" if i == 2 else "Third Floor" if i == 3 else f"{i}th Floor"
        default_stages.append({"stage": f"{floor_label} Structure & Brickwork Combined", "desc": f"Vertical column frames casting, structural slab grid framework, staircase, inner partitioning lines.", "pct": pct_structure_per_floor})
        
    default_stages.append({"stage": "Electrical & Plumbing In-Wall Concealed Works", "desc": "Precision structural chasing tracking, heavy duty fire retardant conduit routing, raw water manifold setup.", "pct": 7.0})
    default_stages.append({"stage": "Floor-wise Internal & External Plaster Completion", "desc": "Rich ratio cement internal plastering coats and weather resilient advanced exterior texture layout plaster setups.", "pct": 8.0})
    
    for i in range(total_floors):
        floor_label = "Ground Floor" if i == 0 else "First Floor" if i == 1 else "Second Floor" if i == 2 else "Third Floor" if i == 3 else f"{i}th Floor"
        default_stages.append({"stage": f"{floor_label} Flooring & Architectural Tiling Work", "desc": f"Premium vitrified tiles slab implementation, engineered stone boundaries, washroom floor to wall layouts.", "pct": 3.0})
        
    default_stages.append({"stage": "Doors, Windows Frame & Security Railings Setup", "desc": "Perimeter wooden door frames insertion, window glass shutters installation, architectural protective barriers layout.", "pct": 6.0})
    default_stages.append({"stage": "Wall Smooth Putty, Base Paint & Premium Fixtures", "desc": "Double smooth coat acrylic base putty application, primary interior coats, luxury modular switches integration.", "pct": 5.0})
    
    allocated_sum = sum(stg['pct'] for stg in default_stages)
    pct_handover = round(max(0.0, 100.0 - allocated_sum), 2)
    default_stages.append({"stage": "Final Custom Detailing, Deep Cleaning & Keys Handover", "desc": "Deep structural sanitization cycles, pristine glass polish work, quality checklists lock and key transitions.", "pct": pct_handover})

edited_stages = []
current_running_sum = 0.0

st.markdown("#### ✏️ Administrative Stage Percentage Overrides Controls")
for idx, stg in enumerate(default_stages):
    st_col1, st_col2 = st.columns([3.6, 1.4])
    with st_col1:
        st.markdown(f"**Stage {idx+1}:** {stg['stage']}")
    with st_col2:
        val_override = st.number_input("Stage %", min_value=0.0, max_value=100.0, value=float(stg['pct']), step=0.01, key=f"stg_override_pct_{idx}")
        edited_stages.append({"stage": stg['stage'], "desc": stg['desc'], "pct": val_override})
        current_running_sum += val_override

current_running_sum = round(current_running_sum, 2)
if current_running_sum != 100.0 and len(edited_stages) > 0:
    difference_offset = round(100.0 - current_running_sum, 2)
    edited_stages[-1]['pct'] = round(edited_stages[-1]['pct'] + difference_offset, 2)

# GENERATE HTML MILESTONE ROWS
payment_schedule_rows = ""
for idx, milestone in enumerate(edited_stages):
    stage_calculated_cost = (milestone['pct'] / 100.0) * net_project_cost
    payment_schedule_rows += f"""
    <tr style="border-bottom: 1px solid #e5e7eb;">
        <td style="padding: 10px; font-size: 12.5px; color: #111827; font-weight: 700; background-color: #fafafa; text-align: center;">{idx+1}</td>
        <td style="padding: 10px; font-size: 13px; color: #111827; font-weight: 700;">{milestone['stage']}</td>
        <td style="padding: 10px; font-size: 12px; color: #4b5563; line-height:1.4;">{milestone['desc']}</td>
        <td style="padding: 10px; font-size: 13px; color: #2563eb; font-weight: 800; text-align: center; background-color: #f0fdf4;">{milestone['pct']:.2f}%</td>
        <td style="padding: 10px; font-size: 13px; color: #111827; font-weight: 800; text-align: right;">Rs. {stage_calculated_cost:,.2f}</td>
    </tr>"""

# COMPLETE DYNAMIC IMAGES MAPPING
images_html = ""
if "Solid Structure" in selected_global_display:
    img_list = [
        {"title": "📐 Plain Elevation", "file": "plain_elevation.jpg"},
        {"title": "RCC Core Frame", "file": "rcc_frame.jpg"},
        {"title": "Robust Brickwork", "file": "brickwork.jpg"},
        {"title": "Plaster Core Work", "file": "plaster.jpg"}
    ]
elif "Essential" in selected_global_display:
    img_list = [
        {"title": "🏙️ Essential Elevation", "file": "elevation_essential.jpg"},
        {"title": "ACP Panel Layout", "file": "acp_elevation.jpg"},
        {"title": "MS Main Gate", "file": "ms_main_gate.jpg"},
        {"title": "MS Railing Setup", "file": "ms_railing.jpg"},
        {"title": "Flush Door System", "file": "flush_door.jpg"},
        {"title": "Basic CP Taps", "file": "basic_taps.jpg"},
        {"title": "Standard WC", "file": "basic_wc.jpg"},
        {"title": "Pop Cornice Styling", "file": "pop_cornice.jpg"} # CHANGE 1: Added here
    ]
else:
    img_list = [
        {"title": "🏛️ HPL Cladding Elevation", "file": "hpl_cladding.jpg"},
        {"title": "Stainless Steel Gate", "file": "ss_main_gate.jpg"},
        {"title": "Designer Main Door", "file": "designer_main_door.jpg"},
        {"title": "Modular Kitchen Matrix", "file": "modular_kitchen.jpg"},
        {"title": "Designer Wardrobe Unit", "file": "designer_wardrobe.jpg"},
        {"title": "Glass Railing System", "file": "glass_railing.jpg"},
        {"title": "SS Staircase Railing", "file": "ss_staircase_railing.jpg"},
        {"title": "Premium Diverter Unit", "file": "diverter.jpg"},
        {"title": "Wall Hung WC System", "file": "wall_hung_wc.jpg"},
        {"title": "Luxury False Ceiling", "file": "false_ceiling.jpg"},
        {"title": "Pop Cornice Styling", "file": "pop_cornice.jpg"},
        {"title": "Granite Slab Finish", "file": "granite_slab.jpg"}
    ]

for img in img_list:
    resolved_src = get_image_source(img['file'])
    images_html += f"""
    <div style="text-align: center; width: 135px; margin: 8px; border: 1px solid #e5e7eb; border-radius: 8px; padding: 8px; background-color: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <img src="{resolved_src}" style="width: 115px; height: 95px; border-radius: 6px; object-fit: cover;" alt="{img['title']}" onerror="this.style.display='none';">
        <div style="font-size: 11px; font-weight: 700; margin-top: 6px; color: #111827; line-height: 1.2;">{img['title']}</div>
    </div>"""

# COMPLETE STRATEGIC BRANDS DECK 
brands_data = [
    {"name": "TATA Steel", "icon": "⛓️"}, {"name": "JINDAL Steel", "icon": "🏗️"},
    {"name": "UltraTech Cement", "icon": "🧱"}, {"name": "Ambuja Cement", "icon": "🦅"},
    {"name": "Kajaria Tiles", "icon": "💎"}, {"name": "Astral Pipes", "icon": "🚰"},
    {"name": "Berger Paints", "icon": "🎨"}, {"name": "Greenply Boards", "icon": "🌳"},
    {"name": "Jaquar Fittings", "icon": "🚿"}, {"name": "Havells Cables", "icon": "⚡"}
]
brands_html = ""
for brand in brands_data:
    brands_html += f"""
    <div style="display: flex; align-items: center; gap: 8px; background: #ffffff; border: 1px solid #e5e7eb; border-radius: 6px; padding: 6px 12px; min-width: 145px; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
        <span style="font-size: 15px;">{brand['icon']}</span>
        <span style="font-size: 11.5px; font-weight: 700; color: #111827;">{brand['name']}</span>
    </div>"""

# SPECIFICATIONS LI GENERATION
excel_specs_html=""

if df_matrix is not None:

    if selected_excel_col in df_matrix.columns:

        for _,row in df_matrix.iterrows():

            category=row.get("Category / Element")
            specification=row.get(selected_excel_col)

            if (
                pd.notna(category)
                and pd.notna(specification)
                and str(specification).strip()!=""
                and "excluded" not in str(specification).lower()
            ):

                excel_specs_html += f"""
                <li style='margin-bottom:8px;'>
                <b>{category}</b>: {specification}
                </li>
                """

    else:

        st.error(
            f"❌ Package column not found: {selected_excel_col}"
        )

        st.write(
            "Available Columns:"
        )

        st.write(
            df_matrix.columns.tolist()
        )

else:

    excel_specs_html="""
    <li>No package specifications loaded.</li>
    """
# FLOOR COST ROW TABLE
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

# MILESTONE SECTION (CHANGE 2: Kept as is, will place in proposal_html below Section 7)
milestone_section_html = ""
if final_ok_switch:
    milestone_section_html = f"""
    <div style="margin-top: 30px; border: 1px solid #d1d5db; border-radius: 12px; padding: 35px; background: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">
        <h3 style="font-size: 14px; font-weight: 800; color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; text-transform: uppercase;">💳 2. Smart Auto-Generated Stage Billing Milestone Matrix</h3>
        <p style="font-size:12px; color:#4b5563; margin-top:5px; margin-bottom:15px;">The construction payouts are strictly calibrated in structured progress cycles matching structural dependencies safely:</p>
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
    </div>
    """

# DYNAMIC PROPOSAL ASSEMBLY 
proposal_html = f"""
<div style="background-color: #ffffff; color: #111827; font-family: 'Segoe UI', Arial, sans-serif; max-width: 850px; margin: 0 auto; padding: 10px;">
    
    <div style="border: 1px solid #d1d5db; border-radius: 12px; padding: 35px; background: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.02); margin-bottom: 30px;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #111827; padding-bottom: 20px;">
            <div>
                <h1 style="margin: 0; color: #111827; font-size: 24px; font-weight: 800; letter-spacing: 0.5px;">SHREE BADREE BUILD TECH PVT. LTD.</h1>
                <div style="font-size: 11px; color: #4b5563; font-weight: 700; margin-top: 4px; letter-spacing: 1px;">AN ISO 9001:2015 CERTIFIED CONSTRUCTION COMPANY</div>
            </div>
            <div style="text-align: right; background-color: #eff6ff; border: 1px solid #bfdbfe; padding: 8px 14px; border-radius: 8px;">
                <span style="font-size: 12px; font-weight: 800; color: #1e40af;">⭐ Google Rating: 4.9/5.0</span>
            </div>
        </div>

        <div style="margin-top: 25px; background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; font-size: 13px;">
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <b>Client Name:</b> {client_name}<br>
                    <b>Site Location:</b> {project_address}<br>
                    <b>Proposal Framework:</b> <span style="color:#2563eb; font-weight:800;">{selected_global_display}</span>
                </div>
                <div style="text-align: right;">
                    <b>Quotation Index No:</b> SBBT/Q/2026/O95<br>
                    <b>Date of Generation:</b> {datetime.date.today().strftime('%d %B %Y')}<br>
                    <b>Architectural Metric:</b> {formatted_plot_ref_str}
                </div>
            </div>
        </div>

        <div style="margin-top: 25px; background-color: #f0fdf4; border-left: 4px solid #16a34a; padding: 15px; font-size: 13.5px; color: #14532d; border-radius: 0 8px 8px 0;">
            <b>Director's Note:</b> {custom_note_text}
        </div>

        <div style="margin-top: 30px;">
            <h3 style="font-size: 14px; font-weight: 800; color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; text-transform: uppercase;">📋 1. Architectural & Additional Structural Matrix</h3>
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
            </div>
        </div>
    </div>

    <div style="border: 1px solid #d1d5db; border-radius: 12px; padding: 35px; background: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.02); margin-bottom: 30px;">
        <h3 style="font-size: 14px; font-weight: 800; color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; text-transform: uppercase;">🛡️ 3. CORE STRUCTURAL COMPLIANCE & QUALITY ASSURANCES</h3>
        <p style="font-size: 12.5px; color: #374151; line-height: 1.6;">Shree Badree Build Tech follows national safety protocols strictly via Indian Standard codes:</p>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px; font-size:12px; margin-top:12px;">
            <div style="background:#f8fafc; padding:12px; border-radius:6px; border:1px solid #e2e8f0;">
                <b style="color:#1e3a8a; display:block; margin-bottom:4px;">🏗️ Structural Steel Ductility (IS 13920)</b>
                Handles strong vibrations smoothly without sudden brittle fractures or joint failures.
            </div>
            <div style="background:#f8fafc; padding:12px; border-radius:6px; border:1px solid #e2e8f0;">
                <b style="color:#1e3a8a; display:block; margin-bottom:4px;">🧱 Foundation Soil Loading (IS 1904)</b>
                Excavation depths are mapped precisely to safe soil bearing capacity records.
            </div>
        </div>
    </div>

    <div style="border: 1px solid #d1d5db; border-radius: 12px; padding: 35px; background: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.02); margin-bottom: 30px;">
        <h3 style="font-size: 14px; font-weight: 800; color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; text-transform: uppercase;">📸 4. Visual Scope Material Inclusion Details</h3>
        <div style="display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; background: #fafafa; padding: 12px; border-radius: 8px; border: 1px solid #e5e7eb; margin-top:10px;">
            {images_html}
        </div>

        <h3 style="font-size: 14px; font-weight: 800; color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; text-transform: uppercase; margin-top: 25px;">🏢 5. Strategic Brand Tie-Ups</h3>
        <div style="display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; background: #fafafa; padding: 12px; border-radius: 8px; border: 1px solid #e5e7eb; margin-top:10px;">
            {brands_html}
        </div>

        <h3 style="font-size: 14px; font-weight: 800; color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; text-transform: uppercase; margin-top: 25px;">🛠️ 6. Technical Specifications & Material Directives</h3>
        <ul style="padding-left: 18px; font-size: 12.5px; color: #374151; line-height: 1.6; margin-top: 10px;">
            {excel_specs_html}
        </ul>
    </div>

    <div style="border: 1px solid #d1d5db; border-radius: 12px; padding: 35px; background: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.02); margin-bottom: 30px;">
        <h3 style="font-size: 14px; font-weight: 800; color: #111827; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; text-transform: uppercase;">🛡️ 7. Commercial Execution Terms & Guarantees</h3>
        <div style="background-color: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 14px; font-size: 12.5px; color: #78350f; line-height: 1.6; margin-top: 10px;">
            • <b>Commercial Validity:</b> Locked for 30 days from layout mapping.<br>
            • <b>Strategic Accords:</b> {additional_reqs_text}
        </div>
        
        {milestone_section_html} </div>

    <div style="border: 1px solid #d1d5db; border-radius: 12px; padding: 35px; background: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.02); margin-top: 30px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-end; font-size: 12px; color: #4b5563;">
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

# HTML CONTAINER FOR PRINT OPERATIONS
full_html_page = f"""<!DOCTYPE html><html><head><meta charset='utf-8'></head>
<body style='margin:0; padding:15px; background-color:#ffffff;'>
{proposal_html}
</body></html>"""

st.write("### 💎 Live Executive Proposal Preview")
st.download_button(
    label="📥 Download & Save Proposal Page",
    data=full_html_page,
    file_name=f"SBBT_Proposal_{client_name.replace(' ', '_')}.html",
    mime="text/html",
    type="primary"
)
st.markdown(proposal_html, unsafe_allow_html=True)
