import streamlit as st

page_stations = st.Page("page1_stations.py", title="Estações", icon=":material/dataset:")
page_data = st.Page("page2_data.py", title="Dados CEDA/INMET", icon=":material/bar_chart:")
page_kge = st.Page("page3_kge.py", title="Comparativo KGE", icon=":material/calculate:")

pg = st.navigation(
        {
            "Estações": [page_stations],
            "Dados CEDA/INMET": [page_data],
            "Comparativo KGE": [page_kge],
        }
    )

pg.run()
