import streamlit as st
import pandas as pd
import datetime
import os
import gspread

# --- GOOGLE SHEET SAVING FUNCTION (Safe Integration) ---
def save_to_sheets(client_name, project_address, total_cost):
    try:
        creds_dict = st.secrets["gcp"]
        gc = gspread.service_account_from_dict(creds_dict)
        sh = gc.open("SBBT_Quotation_Records").sheet1
        row = [str(datetime.date.today()), client_name, project_address, f"Rs. {total_cost:,.2f}"]
        sh.append_row(row)
        return True
    except Exception as e:
        st.error(f"Sheet Save Error: {e}")
        return False

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
        scope_name = st.text_input(f"Scope / Work Name", placeholder="e.g., Heavy Elevator", key=f"sc_name_{idx}", disabled=not toggle_active)
    with sc_col3:
        scope_cost = st.number_input(f"Lumpsum Cost (Rs.)", min_value=0, value=0, step=5000, key=f"sc_cost_{idx}", disabled=not toggle_active)
    if toggle_active and scope_name.strip():
        additional_scopes.append({"name": scope_name.strip(), "cost": scope_cost})

custom_note_text = st.text_area("Client Dedication Note", "We are offering a special commercial advantage for your property.")
additional_reqs_text = st.text_area("Extra Strategic Commitments", "Includes specialized brand structural alignments.")

# MATHEMATICAL PROJECT TOTALS
net_project_cost = sum(item['area'] * item['rate'] for item in floor_data)
for scope in additional_scopes:
    net_project_cost += scope['cost']

# 📊 PAYMENT CONTROL
st.write("---")
st.subheader("💳 Step 4: Smart Milestone Activation Control")
final_ok_switch = st.toggle("🔒 SHOW MILESTONE PAYMENT MATRIX ON PROPOSAL", value=True)

# (Milestone Logic and Proposal HTML Assembly remains exactly as in your original file)
# [Note: Pura code yahan maintain rahega...]

# --- SAVE BUTTON (Integrate safely here) ---
st.write("---")
st.subheader("💾 Data Records")
if st.button("Save Quotation to Google Sheet"):
    if save_to_sheets(client_name, project_address, net_project_cost):
        st.success("✅ Quotation details saved to Google Sheet!")

# --- ORIGINAL DOWNLOAD BUTTON ---
st.write("---")
st.subheader("💎 Live Executive Proposal Preview")
st.download_button(
    label="📥 Download & Save Proposal Page",
    data=full_html_page,
    file_name=f"SBBT_Proposal_{client_name.replace(' ', '_')}.html",
    mime="text/html",
    type="primary"
)
st.markdown(proposal_html, unsafe_allow_html=True)
