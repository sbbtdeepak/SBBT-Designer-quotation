import streamlit as st
import pandas as pd
import datetime
import os

# 1. PAGE SETUP & THEME
st.set_page_config(page_title="SBBT Executive Proposal Engine", page_icon="🏗️", layout="centered")

# IMAGE CONFIGURATION HELPER
def get_image_source(file_name):
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

# INPUT WIDGETS
custom_note_text = st.text_area("Client Dedication Note", "We are offering a special commercial advantage for your property while maintaining premium specifications and long-term value, ensuring trust with zero compromises.")
additional_reqs_text = st.text_area("Extra Strategic Commitments", "Includes specialized brand structural alignments, earthquake resistant RCC frame configuration, and comprehensive support services.")

net_project_cost = sum(item['area'] * item['rate'] for item in floor_data)
for scope in additional_scopes:
    net_project_cost += scope['cost']

# 📊 PAYMENT CONTROL
st.write("---")
st.subheader("💳 Step 4: Smart Milestone Activation Control")
final_ok_switch = st.toggle("🔒 SHOW MILESTONE PAYMENT MATRIX ON PROPOSAL", value=True)

# MILESTONE LOGIC
default_stages = []
# --- [Yahan aapka pura original milestone logic waisa hi rahayga] ---
# (Maine yahan jagah bachane ke liye shortcut use kiya hai, aap apna purana code yahan rakhein)

# IMAGE MAPPING (UPDATED)
if "Solid Structure" in selected_global_display:
    img_list = [{"title": "📐 Plain Elevation", "file": "plain_elevation.jpg"}, {"title": "RCC Core Frame", "file": "rcc_frame.jpg"}, {"title": "Robust Brickwork", "file": "brickwork.jpg"}, {"title": "Plaster Core Work", "file": "plaster.jpg"}]
elif "Essential" in selected_global_display:
    img_list = [
        {"title": "🏙️ Essential Elevation", "file": "elevation_essential.jpg"},
        {"title": "ACP Panel Layout", "file": "acp_elevation.jpg"},
        {"title": "MS Main Gate", "file": "ms_main_gate.jpg"},
        {"title": "MS Railing Setup", "file": "ms_railing.jpg"},
        {"title": "Flush Door System", "file": "flush_door.jpg"},
        {"title": "Basic CP Taps", "file": "basic_taps.jpg"},
        {"title": "Standard WC", "file": "basic_wc.jpg"},
        {"title": "Pop Cornice Styling", "file": "pop_cornice.jpg"} # <--- Yahan add kiya
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
        {"title": "Granite Slab Finish", "file": "granite_slab.jpg"}
        # Pop Cornice yahan se hata diya
    ]

# PROPOSAL ASSEMBLY (Milestone shifted)
milestone_section_html = f"..." if final_ok_switch else "" # Apka original logic

proposal_html = f"""
... (Aapka original HTML structure) ...
{milestone_section_html}
...
"""

# PDF DOWNLOAD BUTTON
st.download_button("📥 Download & Save Proposal", data=full_html_page, file_name="proposal.html", mime="text/html")
st.markdown(proposal_html, unsafe_allow_html=True)
