import streamlit as st

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_file_path = "./resources/style/style.css"
load_css(css_file_path)

page_about = st.Page("pages/0_ℹ️_About.py", title="Sobre", icon=":material/info:")
page_started = st.Page("pages/1_🌟_Started.py", title="Início", icon=":material/start:")
page_stations = st.Page("pages/2_📊_Stations.py", title="Visualizar/Gerenciar", icon=":material/dataset:")
page_process_stations = st.Page("pages/3_💾_Process_Stations.py", title="Processar Estações", icon=":material/memory:")
page_ceda_data = st.Page("pages/4_📈_CEDA_Data.py", title="Dados CEDA", icon=":material/bar_chart:")
page_inmet_data = st.Page("pages/5_📊_INMET_Data.py", title="Dados INMET", icon=":material/bar_chart:")
page_kge = st.Page("pages/6_🔢_KGE.py", title="KGE - Kling-Gupta Efficiency", icon=":material/calculate:")

pg = st.navigation(
        {
            "Data Extract from CEDA": [page_about, page_started],
            "Estações": [page_stations, page_process_stations],
            "Dados": [page_ceda_data, page_inmet_data],
            "Comparativo": [page_kge],
        }
    )

pg.run()
