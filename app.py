import streamlit as st
import pandas as pd
import datetime
import os

# 1. PAGE SETUP
st.set_page_config(page_title="SBBT Executive Proposal Engine", page_icon="🏗️", layout="centered")

def get_image_source(file_name):
    github_username = "sbbtdeepak"  
    github_repo = "SBBT-Designer-quotation"  
    return f"https://raw.githubusercontent.com/{github_username}/{github_repo}/main/images/{file_name}"

# 2. MATRIX LOADER
@st.cache_data
def load_sbbt_matrix():
    if os.path.exists("SBBT_Master_Quotation_Matrix.xlsx"):
        return pd.read_excel("SBBT_Master_Quotation_Matrix.xlsx", sheet_name="AI Master Matrix")
    return None

df_matrix = load_sbbt_matrix()

# 3. AUTHENTICATION
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("🏗️ SBBT Enterprise Portal")
    if st.button("Login"):
        st.session_state['authenticated'] = True
        st.rerun()
    st.stop()

# 4. ENGINE CONTROLS
st.title("🎛️ SBBT Estimation Control")
package_options = {
    "Solid Structure Core": "Core Shell Package", 
    "Essential Finishing": "Essential Package", 
    "Premium Luxury Profile": "Premium Luxury Package"
}

col1, col2 = st.columns(2)
with col1:
    client_name = st.text_input("Client Name", "Arvind")
    selected_global_display = st.selectbox("Select Master Package", list(package_options.keys()), index=1)
    selected_excel_col = package_options[selected_global_display]

with col2:
    plot_area_yd = st.number_input("Plot Area (Sq. Yards)", value=100)
    total_floors = st.slider("Floors", 1, 12, 4)

# 5. INPUT WIDGETS
custom_note_text = st.text_area("Director's Note", "We are offering a special commercial advantage for your property...")
additional_reqs_text = st.text_area("Extra Commitments", "Includes specialized brand structural alignments...")

# 6. DYNAMIC IMAGE MAPPING (FIXED: POP Cornice is now in Essential)
images_html = ""
if "Solid Structure" in selected_global_display:
    img_list = [{"title": "RCC Frame", "file": "rcc_frame.jpg"}]
elif "Essential" in selected_global_display:
    img_list = [
        {"title": "ACP Elevation", "file": "acp_elevation.jpg"},
        {"title": "POP Cornice", "file": "pop_cornice.jpg"}, 
        {"title": "Flush Door", "file": "flush_door.jpg"}
    ]
else: # Premium
    img_list = [
        {"title": "HPL Cladding", "file": "hpl_cladding.jpg"},
        {"title": "Modular Kitchen", "file": "modular_kitchen.jpg"},
        {"title": "Luxury Ceiling", "file": "false_ceiling.jpg"}
    ]

for img in img_list:
    images_html += f"""
    <div style="text-align: center; width: 120px; margin: 5px; border: 1px solid #ccc; padding: 5px;">
        <img src="{get_image_source(img['file'])}" style="width: 100px; height: 80px; object-fit: cover;">
        <div style="font-size: 10px; font-weight: bold;">{img['title']}</div>
    </div>"""

# 7. FINAL PROPOSAL HTML
proposal_html = f"""
<div style="font-family: sans-serif; padding: 30px; border: 2px solid #333; max-width: 800px; margin: auto;">
    <h1 style="color: #111;">SHREE BADREE BUILD TECH PVT. LTD.</h1>
    <p><b>Client Name:</b> {client_name}</p>
    <div style="background: #f0fdf4; padding: 15px; border-left: 5px solid #16a34a;">
        <b>Director's Note:</b> {custom_note_text}
    </div>
    
    <h3 style="margin-top: 30px;">Visual Material Inclusions</h3>
    <div style="display: flex; flex-wrap: wrap;">{images_html}</div>
    
    <hr style="margin: 30px 0;">
    <p><b>Extra Strategic Commitments:</b></p>
    <p style="font-size: 14px; color: #444;">{additional_reqs_text}</p>
</div>
"""

st.markdown(proposal_html, unsafe_allow_html=True)

# 8. DOWNLOAD BUTTON
st.download_button(
    label="📥 Download Proposal as HTML",
    data=proposal_html,
    file_name=f"SBBT_Proposal_{client_name}.html",
    mime="text/html"
)
