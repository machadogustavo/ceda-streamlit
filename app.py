import streamlit as st

page_about = st.Page("pages/page0_about.py", title="Sobre", icon=":material/info:")
page_started = st.Page("pages/page1_started.py", title="Início", icon=":material/start:")
page_stations = st.Page("pages/page2_stations.py", title="Tabela de Estações", icon=":material/dataset:")
page_ceda_data = st.Page("pages/page3_ceda_data.py", title="Dados CEDA", icon=":material/bar_chart:")
page_inmet_data = st.Page("pages/page4_inmet_data.py", title="Dados INMET", icon=":material/bar_chart:")
page_kge = st.Page("pages/page5_kge.py", title="Comparativo KGE", icon=":material/calculate:")

pg = st.navigation(
        {
            "Data Extract from CEDA": [page_about,page_started],
            "Estações": [page_stations],
            "Dados": [page_ceda_data, page_inmet_data],
            "Comparativo": [page_kge],
        }
    )

pg.run()
