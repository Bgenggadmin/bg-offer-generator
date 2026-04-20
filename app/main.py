"""
B&G Engineering — Offer Generator (Streamlit UI)

Branded UI for generating techno-commercial offer DOCX documents.
"""
import streamlit as st
from pathlib import Path
from datetime import date

from app.utils.brand import BRAND, COMPANY, OFFER_TOC
from app.utils.default_data import default_offer_data
from app.modules.docx_generator import generate_offer_docx
from app.utils.form_template import generate_form_template_xlsx
from app.utils.bridge import (
    parse_process_design_json, bridge_to_offer_data, summarize_bridge_result,
)


# ---------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="B&G Offer Generator",
    page_icon="🔧",
    layout="wide",
)

# Inject custom CSS for B&G branding
st.markdown(f"""
<style>
    .main-header {{
        background: linear-gradient(135deg, {BRAND['primary_red']} 0%, {BRAND['accent_pink']} 100%);
        padding: 20px 30px;
        border-radius: 8px;
        margin-bottom: 24px;
    }}
    .main-header h1 {{
        color: white !important;
        margin: 0;
        font-size: 28px;
    }}
    .main-header p {{
        color: rgba(255,255,255,0.9) !important;
        margin: 4px 0 0 0;
        font-size: 14px;
    }}
    .stButton > button[kind="primary"] {{
        background: {BRAND['primary_red']};
        color: white;
        border: none;
    }}
    .stButton > button[kind="primary"]:hover {{
        background: {BRAND['accent_pink']};
    }}
    div[data-testid="stExpander"] {{
        border: 1px solid #e0e0e0;
        border-radius: 6px;
    }}
    .section-tag {{
        display: inline-block;
        background: {BRAND['accent_pink']};
        color: white;
        padding: 2px 10px;
        border-radius: 3px;
        font-size: 11px;
        font-weight: bold;
    }}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------
# BRANDED HEADER
# ---------------------------------------------------------------------
def _render_header():
    col1, col2 = st.columns([1, 4])
    with col1:
        logo = Path("app/assets/bg_logo.png")
        if logo.exists():
            st.image(str(logo), width=140)
    with col2:
        st.markdown(f"""
        <div class="main-header">
            <h1>Techno-Commercial Offer Generator</h1>
            <p>B&G Engineering Industries · Responsible towards water · Hyderabad</p>
        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------------------
# SESSION STATE HELPERS
# ---------------------------------------------------------------------
def _init_state():
    if "offer_data" not in st.session_state:
        st.session_state.offer_data = default_offer_data()


def _reset_data():
    st.session_state.offer_data = default_offer_data()
    st.success("Form reset to defaults ✓")
    st.rerun()


# ---------------------------------------------------------------------
# MAIN APP
# ---------------------------------------------------------------------
def main():
    _init_state()
    _render_header()

    tabs = st.tabs([
        "① Cover & Client",
        "② Executive Summary",
        "③ Process Description",
        "④ Economics / OPEX",
        "⑤ Technical & Utilities",
        "⑥ Scope of Supply",
        "⑦ Scope Matrix",
        "⑧ Pricing & Terms",
        "🚀 Generate",
        "📥 Templates / Bridge",
    ])

    with tabs[0]:
        _tab_cover()
    with tabs[1]:
        _tab_executive_summary()
    with tabs[2]:
        _tab_process_description()
    with tabs[3]:
        _tab_economics()
    with tabs[4]:
        _tab_technical()
    with tabs[5]:
        _tab_scope()
    with tabs[6]:
        _tab_scope_matrix()
    with tabs[7]:
        _tab_pricing()
    with tabs[8]:
        _tab_generate()
    with tabs[9]:
        _tab_templates()


# ---------------------------------------------------------------------
# TAB 1: COVER & CLIENT
# ---------------------------------------------------------------------
def _tab_cover():
    st.subheader("Cover Page & Client Details")
    st.caption("Data appears on the offer's front page and cover letter.")

    d = st.session_state.offer_data["cover"]
    c1, c2 = st.columns(2)
    with c1:
        d["quote_ref"] = st.text_input("Quote Reference", value=d["quote_ref"],
                                         help="e.g. BG/ECOX-ZLD/26-27/2948 R1")
        d["quote_date"] = st.text_input("Quotation Date (YYYY-MM-DD)", value=str(d["quote_date"]))
        d["submitted_to"] = st.text_input("Submitted to (Client)", value=d["submitted_to"])
        d["location"] = st.text_input("Location", value=d["location"])
        d["capacity_kld"] = st.number_input("Capacity (KLD)",
                                              value=int(d["capacity_kld"]),
                                              min_value=1, max_value=5000, step=10)
    with c2:
        d["prepared_by"] = st.text_input("Prepared By", value=d["prepared_by"])
        d["contact_details"] = st.text_input("Contact Details", value=d["contact_details"])
        d["email"] = st.text_input("E-mail", value=d["email"])
        d["kind_attn"] = st.text_input("Kind Attention (Client Contact Name / Role)",
                                         value=d["kind_attn"])
        d["discussion_date"] = st.text_input("Discussion Date (for cover letter)",
                                               value=d["discussion_date"],
                                               help="e.g. 11/04/2026 — used in the cover letter intro")

    d["subject"] = st.text_input("Subject Line", value=d["subject"])


# ---------------------------------------------------------------------
# TAB 2: EXECUTIVE SUMMARY
# ---------------------------------------------------------------------
def _tab_executive_summary():
    st.subheader("PART I — Executive Summary")
    st.caption("A well-crafted summary is what the client's AI will see first. "
                "Keep it factual, quantitative, and specific to your capabilities.")
    st.session_state.offer_data["executive_summary"] = st.text_area(
        "Executive Summary (editable)",
        value=st.session_state.offer_data["executive_summary"],
        height=400,
        help="This text appears under 'PART I — Executive Summary'. Edit for company context or project emphasis.",
    )


# ---------------------------------------------------------------------
# TAB 3: PROCESS DESCRIPTION
# ---------------------------------------------------------------------
def _tab_process_description():
    st.subheader("PART II — Process Description")
    st.caption("Written explanation of how each unit works. Use {n_effects} "
                "placeholder in MEE text — it's replaced automatically.")

    pd = st.session_state.offer_data["process_description"]

    pd["n_effects"] = st.slider("Number of MEE Effects",
                                  min_value=2, max_value=7,
                                  value=int(pd.get("n_effects", 4)))

    with st.expander("🧪 Stripper Process Description", expanded=True):
        pd["stripper"] = st.text_area("Stripper text", value=pd["stripper"],
                                         height=200, key="stripper_desc")

    with st.expander("💧 MEE Process Description"):
        pd["mee"] = st.text_area("MEE text (use `{n_effects}` for effect count)",
                                   value=pd["mee"], height=300, key="mee_desc")

    with st.expander("🌡 ATFD Process Description"):
        pd["atfd"] = st.text_area("ATFD text", value=pd["atfd"],
                                    height=300, key="atfd_desc")


# ---------------------------------------------------------------------
# TAB 4: ECONOMICS / OPEX
# ---------------------------------------------------------------------
def _tab_economics():
    st.subheader("PART IV — Plant Economics & OPEX Comparison")
    st.caption("BG ECOX-ZLD advantage — side-by-side with conventional evaporation.")

    econ = st.session_state.offer_data["economics"]

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Conventional**")
        econ["conventional_steam_kgh"] = st.number_input(
            "Steam Consumption (Kg/h)",
            value=int(econ["conventional_steam_kgh"]),
            key="conv_steam"
        )
        econ["conventional_annual_steam_tons"] = st.number_input(
            "Annual Steam Usage (tons/yr)",
            value=int(econ["conventional_annual_steam_tons"]),
            key="conv_ann_steam"
        )
        econ["conventional_annual_cost_cr"] = st.number_input(
            "Annual Operating Cost (Cr/yr)",
            value=float(econ["conventional_annual_cost_cr"]),
            step=0.01, key="conv_cost"
        )
    with c2:
        st.markdown("**BG ECOX-ZLD**")
        econ["ecox_steam_kgh"] = st.number_input(
            "Steam Consumption (Kg/h)", value=int(econ["ecox_steam_kgh"]),
            key="ecox_steam"
        )
        econ["ecox_annual_steam_tons"] = st.number_input(
            "Annual Steam Usage (tons/yr)",
            value=int(econ["ecox_annual_steam_tons"]),
            key="ecox_ann_steam"
        )
        econ["ecox_annual_cost_cr"] = st.number_input(
            "Annual Operating Cost (Cr/yr)",
            value=float(econ["ecox_annual_cost_cr"]),
            step=0.01, key="ecox_cost"
        )
    with c3:
        st.markdown("**Savings**")
        econ["steam_reduction_pct"] = st.number_input(
            "Steam Reduction %",
            value=int(econ["steam_reduction_pct"]), key="sav_pct"
        )
        econ["annual_steam_savings_tons"] = st.number_input(
            "Annual Steam Savings (tons/yr)",
            value=int(econ["annual_steam_savings_tons"]),
            key="sav_tons"
        )
        econ["annual_savings_lakhs"] = st.number_input(
            "Annual Cost Savings (Lakhs/yr)",
            value=int(econ["annual_savings_lakhs"]),
            key="sav_lakhs"
        )

    st.divider()
    c1, c2, c3 = st.columns(3)
    econ["operating_hours_day"] = c1.number_input(
        "Operating Hours/Day", value=int(econ["operating_hours_day"]),
        min_value=1, max_value=24, key="op_h"
    )
    econ["operating_days_year"] = c2.number_input(
        "Operating Days/Year", value=int(econ["operating_days_year"]),
        min_value=1, max_value=365, key="op_d"
    )
    econ["steam_cost_inr_kg"] = c3.number_input(
        "Steam Cost (INR/Kg)", value=float(econ["steam_cost_inr_kg"]),
        step=0.1, key="steam_c"
    )


# ---------------------------------------------------------------------
# TAB 5: TECHNICAL & UTILITIES
# ---------------------------------------------------------------------
def _tab_technical():
    st.subheader("PART V — Technical Details & Utilities")

    data = st.session_state.offer_data

    # Feed parameters
    with st.expander("Feed Parameters", expanded=True):
        fp = data["feed_parameters"]
        c1, c2 = st.columns(2)
        with c1:
            fp["capacity_kld"] = st.number_input("Capacity (KLD)",
                                                   value=int(fp["capacity_kld"]), key="fp_cap")
            fp["feed_ph"] = st.text_input("Feed pH", value=str(fp["feed_ph"]), key="fp_ph")
            fp["total_cod_ppm"] = st.number_input("Total COD (PPM)",
                                                    value=int(fp["total_cod_ppm"]), key="fp_cod")
            fp["volatile_organic_solvents_ppm"] = st.number_input(
                "Volatile Organic Solvents (PPM)",
                value=int(fp["volatile_organic_solvents_ppm"]), key="fp_vos"
            )
            fp["total_solids_pct"] = st.number_input(
                "Total Solids (% w/w)",
                value=float(fp["total_solids_pct"]), step=0.1, key="fp_ts"
            )
            fp["feed_temp_c"] = st.number_input(
                "Feed Temp (°C)", value=int(fp["feed_temp_c"]), key="fp_T"
            )
        with c2:
            fp["suspended_solids_ppm"] = st.text_input(
                "Suspended Solids (PPM)",
                value=str(fp["suspended_solids_ppm"]), key="fp_ss"
            )
            fp["total_hardness_ppm"] = st.text_input(
                "Total Hardness (PPM)",
                value=str(fp["total_hardness_ppm"]), key="fp_th"
            )
            fp["silica_ppm"] = st.text_input(
                "Silica (PPM)", value=str(fp["silica_ppm"]), key="fp_si"
            )
            fp["free_chloride_ppm"] = st.text_input(
                "Free Chloride (PPM)",
                value=str(fp["free_chloride_ppm"]), key="fp_cl"
            )
            fp["feed_nature"] = st.text_input(
                "Feed Nature", value=fp["feed_nature"], key="fp_nat"
            )

    # Technical Specs
    with st.expander("Stripper Technical Specs"):
        s = data["technical_specs"]["stripper"]
        c1, c2 = st.columns(2)
        with c1:
            s["type"] = st.text_input("Stripper Type", value=s["type"], key="s_type")
            s["feed_kgh"] = st.number_input("Feed Inlet (Kg/h)",
                                              value=int(s["feed_kgh"]), key="s_feed")
        with c2:
            s["distillate_kgh"] = st.number_input("Top Distillate Out (Kg/h)",
                                                    value=int(s["distillate_kgh"]), key="s_dist")
            s["distillate_composition"] = st.text_input(
                "Distillate Composition",
                value=s["distillate_composition"], key="s_comp"
            )
        s["bottoms_kgh"] = st.number_input("Stripper Bottoms Out (Kg/h)",
                                             value=int(s["bottoms_kgh"]), key="s_bot")

    with st.expander("MEE Technical Specs"):
        m = data["technical_specs"]["mee"]
        c1, c2 = st.columns(2)
        with c1:
            m["type"] = st.text_input("MEE Type", value=m["type"], key="m_type")
            m["configuration"] = st.text_input("Configuration",
                                                 value=m["configuration"], key="m_cfg")
            m["feed_kgh"] = st.number_input("Feed Inlet (Kg/h)",
                                              value=int(m["feed_kgh"]), key="m_feed")
            m["feed_solids_pct"] = st.number_input("Feed Solids (%)",
                                                      value=float(m["feed_solids_pct"]),
                                                      step=0.01, key="m_fs")
        with c2:
            m["evaporation_kgh"] = st.number_input("Water Evaporation (Kg/h)",
                                                      value=int(m["evaporation_kgh"]), key="m_evap")
            m["concentrate_kgh"] = st.number_input("Concentrate Out (Kg/h)",
                                                     value=int(m["concentrate_kgh"]), key="m_conc")
            m["concentrate_solids_pct"] = st.number_input(
                "Concentrate Solids (%)",
                value=int(m["concentrate_solids_pct"]), key="m_cs"
            )

    with st.expander("ATFD Technical Specs"):
        a = data["technical_specs"]["atfd"]
        c1, c2 = st.columns(2)
        with c1:
            a["type"] = st.text_input("ATFD Type", value=a["type"], key="a_type")
            a["feed_kgh"] = st.number_input("Feed Inlet (Kg/h)",
                                              value=int(a["feed_kgh"]), key="a_feed")
            a["feed_solids_pct"] = st.number_input("Feed Solids (%)",
                                                      value=int(a["feed_solids_pct"]), key="a_fs")
        with c2:
            a["evaporation_kgh"] = st.number_input("Water Evaporation (Kg/h)",
                                                      value=int(a["evaporation_kgh"]), key="a_evap")
            a["product_kgh"] = st.number_input("Product Out (Kg/h)",
                                                 value=int(a["product_kgh"]), key="a_prod")
            a["product_moisture_pct"] = st.text_input("Product Moisture (%)",
                                                         value=str(a["product_moisture_pct"]),
                                                         key="a_moist")

    with st.expander("Utilities"):
        u = data["utilities"]
        c1, c2 = st.columns(2)
        with c1:
            u["stripper_steam"]["param"] = st.text_input(
                "Stripper Steam Params",
                value=u["stripper_steam"]["param"], key="u_ss_p"
            )
            u["stripper_steam"]["value_kgh"] = st.number_input(
                "Stripper Steam (Kg/h)",
                value=int(u["stripper_steam"]["value_kgh"]), key="u_ss_v"
            )
            u["mee_steam"]["param"] = st.text_input(
                "MEE Steam Params",
                value=u["mee_steam"]["param"], key="u_ms_p"
            )
            u["mee_steam"]["value_kgh"] = st.number_input(
                "MEE Steam (Kg/h)",
                value=int(u["mee_steam"]["value_kgh"]), key="u_ms_v"
            )
            u["mee_steam"]["steam_economy"] = st.number_input(
                "Steam Economy (Kg/Kg)",
                value=float(u["mee_steam"]["steam_economy"]),
                step=0.1, key="u_ms_se"
            )
            u["atfd_steam"]["param"] = st.text_input(
                "ATFD Steam Params",
                value=u["atfd_steam"]["param"], key="u_as_p"
            )
            u["atfd_steam"]["value_kgh"] = st.number_input(
                "ATFD Steam (Kg/h)",
                value=int(u["atfd_steam"]["value_kgh"]), key="u_as_v"
            )
        with c2:
            u["power_consumption_kwh"] = st.number_input(
                "Power Consumption (kWh)",
                value=int(u["power_consumption_kwh"]), key="u_pwr_c"
            )
            u["power_installed_kw"] = st.number_input(
                "Power Installed (kW, incl. standby)",
                value=int(u["power_installed_kw"]), key="u_pwr_i"
            )
            u["cooling_water_m3h"] = st.number_input(
                "Cooling Water (m³/h)",
                value=int(u["cooling_water_m3h"]), key="u_cw"
            )
            u["cooling_water_temps"] = st.text_input(
                "CW Temperatures",
                value=u["cooling_water_temps"], key="u_cw_t"
            )
            u["compressed_air_nm3h"] = st.text_input(
                "Compressed Air (Nm³/h)",
                value=u["compressed_air_nm3h"], key="u_ca_f"
            )
            u["compressed_air_pressure"] = st.text_input(
                "Compressed Air Pressure",
                value=u["compressed_air_pressure"], key="u_ca_p"
            )

    with st.expander("Performance Guarantee Bullets"):
        pg_text = "\n".join(data["performance_guarantee"])
        new_pg = st.text_area("One bullet per line", value=pg_text, height=300,
                                key="pg_area")
        data["performance_guarantee"] = [
            line.strip() for line in new_pg.split("\n") if line.strip()
        ]


# ---------------------------------------------------------------------
# TAB 6: SCOPE OF SUPPLY
# ---------------------------------------------------------------------
def _tab_scope():
    st.subheader("PART VI — Scope of Supply")
    st.caption("Edit equipment lists, specs, and quantities per section. "
                "B&G Scope / Buyer Scope determines who's responsible.")

    import pandas as pd
    data = st.session_state.offer_data

    sub_tabs = st.tabs(["Stripper System", "MEE System", "ATFD System", "Instruments"])

    with sub_tabs[0]:
        df = pd.DataFrame(data["scope_stripper"])
        edited = st.data_editor(df, use_container_width=True, num_rows="dynamic",
                                 key="sc_strip",
                                 column_config={
                                     "bg_scope": st.column_config.CheckboxColumn("B&G"),
                                     "buyer_scope": st.column_config.CheckboxColumn("Buyer"),
                                     "specification": st.column_config.TextColumn("Specification", width="large"),
                                 })
        data["scope_stripper"] = edited.to_dict("records")

    with sub_tabs[1]:
        df = pd.DataFrame(data["scope_mee"])
        edited = st.data_editor(df, use_container_width=True, num_rows="dynamic",
                                 key="sc_mee",
                                 column_config={
                                     "bg_scope": st.column_config.CheckboxColumn("B&G"),
                                     "buyer_scope": st.column_config.CheckboxColumn("Buyer"),
                                     "specification": st.column_config.TextColumn("Specification", width="large"),
                                 })
        data["scope_mee"] = edited.to_dict("records")

    with sub_tabs[2]:
        df = pd.DataFrame(data["scope_atfd"])
        edited = st.data_editor(df, use_container_width=True, num_rows="dynamic",
                                 key="sc_atfd",
                                 column_config={
                                     "bg_scope": st.column_config.CheckboxColumn("B&G"),
                                     "buyer_scope": st.column_config.CheckboxColumn("Buyer"),
                                     "specification": st.column_config.TextColumn("Specification", width="large"),
                                 })
        data["scope_atfd"] = edited.to_dict("records")

    with sub_tabs[3]:
        df = pd.DataFrame(data["instruments"])
        edited = st.data_editor(df, use_container_width=True, num_rows="dynamic",
                                 key="sc_inst")
        data["instruments"] = edited.to_dict("records")


# ---------------------------------------------------------------------
# TAB 7: SCOPE MATRIX + BATTERY LIMITS
# ---------------------------------------------------------------------
def _tab_scope_matrix():
    st.subheader("PART VII & VIII — Battery Limits & Scope Matrix")

    import pandas as pd
    data = st.session_state.offer_data

    with st.expander("Battery Limits (PART VII)", expanded=True):
        bl_text = "\n".join(data["battery_limits"])
        new_bl = st.text_area("One line per battery limit item",
                                value=bl_text, height=300, key="bl_area")
        data["battery_limits"] = [
            line.strip() for line in new_bl.split("\n") if line.strip()
        ]

    with st.expander("Scope Matrix (PART VIII)", expanded=True):
        df = pd.DataFrame(data["scope_matrix"])
        edited = st.data_editor(df, use_container_width=True, num_rows="dynamic",
                                 key="scope_mat",
                                 column_config={
                                     "bg": st.column_config.CheckboxColumn("B&G"),
                                     "client": st.column_config.CheckboxColumn("Client"),
                                     "description": st.column_config.TextColumn("Description", width="large"),
                                 })
        data["scope_matrix"] = edited.to_dict("records")


# ---------------------------------------------------------------------
# TAB 8: PRICING & TERMS
# ---------------------------------------------------------------------
def _tab_pricing():
    st.subheader("PART X — Price & Commercial Terms")

    pr = st.session_state.offer_data["pricing"]

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Option 1**")
        pr["option1_moc"] = st.text_input("MOC Option 1", value=pr["option1_moc"], key="p_o1_moc")
        pr["option1_equipment_price_cr"] = st.number_input(
            "Equipment Price (Cr)",
            value=float(pr["option1_equipment_price_cr"]), step=0.01, key="p_o1_eq"
        )
        pr["option1_install_lakhs"] = st.number_input(
            "Install & Commission (Lakhs)",
            value=float(pr["option1_install_lakhs"]), step=1.0, key="p_o1_ic"
        )
        pr["option1_total_cr"] = st.number_input(
            "Total (Cr)", value=float(pr["option1_total_cr"]),
            step=0.01, key="p_o1_tot"
        )
    with c2:
        st.markdown("**Option 2**")
        pr["option2_moc"] = st.text_input("MOC Option 2", value=pr["option2_moc"], key="p_o2_moc")
        pr["option2_equipment_price_cr"] = st.number_input(
            "Equipment Price (Cr)",
            value=float(pr["option2_equipment_price_cr"]), step=0.01, key="p_o2_eq"
        )
        pr["option2_install_lakhs"] = st.number_input(
            "Install & Commission (Lakhs)",
            value=float(pr["option2_install_lakhs"]), step=1.0, key="p_o2_ic"
        )
        pr["option2_total_cr"] = st.number_input(
            "Total (Cr)", value=float(pr["option2_total_cr"]),
            step=0.01, key="p_o2_tot"
        )

    st.divider()
    c1, c2 = st.columns(2)
    pr["location_dap"] = c1.text_input("Location (DAP)", value=pr["location_dap"], key="p_loc")
    pr["price_validity_days"] = c2.number_input(
        "Price Validity (Days)", value=int(pr["price_validity_days"]),
        min_value=1, max_value=365, key="p_val"
    )

    st.markdown("**Payment Terms** (one line each)")
    pt_text = "\n".join(pr["payment_terms"])
    new_pt = st.text_area("Payment Terms", value=pt_text, height=180, key="pt_area")
    pr["payment_terms"] = [line.strip() for line in new_pt.split("\n") if line.strip()]

    st.markdown("**Delivery Timeline**")
    dt = pr["delivery_timeline"]
    dt["supply_option1"] = st.text_input("Supply Option 1", value=dt["supply_option1"], key="dt_o1")
    dt["supply_option2"] = st.text_input("Supply Option 2", value=dt["supply_option2"], key="dt_o2")
    dt["installation"] = st.text_input("Installation", value=dt["installation"], key="dt_i")
    dt["commissioning"] = st.text_input("Commissioning", value=dt["commissioning"], key="dt_c")


# ---------------------------------------------------------------------
# TAB 9: GENERATE
# ---------------------------------------------------------------------
def _tab_generate():
    st.subheader("🚀 Generate Offer DOCX")
    st.caption("Once all tabs are complete, click below to generate the Word document. "
                "It contains all 11 parts with B&G branding, logos, and formatted tables.")

    d = st.session_state.offer_data

    # Summary
    c1, c2, c3 = st.columns(3)
    c1.metric("Client", d["cover"]["submitted_to"])
    c2.metric("Capacity", f"{d['cover']['capacity_kld']} KLD")
    c3.metric("Option 1 Total", f"₹{d['pricing']['option1_total_cr']:.2f} Cr")

    c1, c2, c3 = st.columns(3)
    c1.metric("Stripper Feed", f"{d['technical_specs']['stripper']['feed_kgh']} kg/h")
    c2.metric("MEE Effects", d['process_description']['n_effects'])
    c3.metric("ATFD Product", f"{d['technical_specs']['atfd']['product_kgh']} kg/h")

    st.divider()

    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("🔨 Generate Offer DOCX", type="primary", use_container_width=True):
            with st.spinner("Building DOCX..."):
                try:
                    docx_bytes = generate_offer_docx(
                        d,
                        logo_path="app/assets/bg_logo.png",
                        tagline_path="app/assets/bg_tagline.png",
                        hero_path="app/assets/bg_hero_plant.png",
                    )
                    st.session_state.generated_docx = docx_bytes
                    st.success(f"✅ Generated: {len(docx_bytes)/1024:.1f} KB")
                except Exception as e:
                    st.error(f"Generation failed: {e}")
                    import traceback
                    st.code(traceback.format_exc())

    with col2:
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            _reset_data()

    if "generated_docx" in st.session_state:
        st.download_button(
            label="📥 Download Offer DOCX",
            data=st.session_state.generated_docx,
            file_name=f"Quote_{d['cover']['quote_ref'].replace('/', '_')}_{d['cover']['capacity_kld']}KLD.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )


# ---------------------------------------------------------------------
# TAB 10: TEMPLATES & BRIDGE
# ---------------------------------------------------------------------
def _tab_templates():
    st.subheader("📥 Form Template & Process Design Bridge")

    # --- Download form template ---
    with st.expander("📋 Download Excel Form Template", expanded=True):
        st.markdown("""
        Download a pre-filled Excel template that trainee engineers can fill offline
        with client-specific details. Once filled, upload it below to auto-populate the form.
        """)
        if st.button("Generate Excel Form Template", key="gen_xlsx"):
            xlsx_bytes = generate_form_template_xlsx()
            st.session_state.xlsx_template = xlsx_bytes
        if "xlsx_template" in st.session_state:
            st.download_button(
                label="📥 Download Form Template (.xlsx)",
                data=st.session_state.xlsx_template,
                file_name="BG_Offer_Form_Template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

    # --- Bridge from process design JSON ---
    with st.expander("🔗 Import from Process Design (bg_process_design JSON)", expanded=True):
        st.markdown("""
        If you've already run the design in the **bg_process_design** app and downloaded
        the **Full Project JSON**, upload it here to auto-populate technical specs,
        utilities, and economics. You'll only need to fill commercial terms manually.
        """)
        uploaded = st.file_uploader("Upload full_project.json", type=["json"],
                                      key="pd_json")
        if uploaded:
            try:
                content = uploaded.read().decode("utf-8")
                process_json = parse_process_design_json(content)

                if st.button("🔀 Import into offer form", type="primary", key="btn_bridge"):
                    new_data = bridge_to_offer_data(
                        process_json,
                        existing_data=st.session_state.offer_data,
                    )
                    st.session_state.offer_data = new_data

                    st.success("✅ Process design imported successfully!")
                    summary = summarize_bridge_result(process_json, new_data)
                    for line in summary:
                        st.markdown(line)
                    st.info("Now visit the other tabs to review and customize, then go to 'Generate' to build the DOCX.")
            except Exception as e:
                st.error(f"Failed to parse JSON: {e}")

    # --- About ---
    with st.expander("ℹ️ About This Tool"):
        st.markdown(f"""
        **B&G Offer Generator** — separate from `bg_process_design` to keep concerns clean.

        **Features:**
        - Generates branded DOCX matching the 11-part offer template
        - Uses B&G logo, 'Responsible towards water' tagline, and red/pink brand colors
        - Full flexibility to edit any text section
        - Bridge from `bg_process_design` JSON to auto-fill technical specs
        - Excel template for offline data collection by trainees

        **Company:** {COMPANY['name']}
        **Managing Partner:** {COMPANY['managing_partner']}
        **Location:** {COMPANY['address']}
        """)


if __name__ == "__main__":
    main()
