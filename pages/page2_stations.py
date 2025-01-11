import streamlit as st
from tabs import page1_tab1_visualize_stations, page1_tab2_process_stations

tab1, tab2 = st.tabs(["Tabela de Estações","Processar Estações"])

with tab1:
    page1_tab1_visualize_stations.render()

with tab2:
    page1_tab2_process_stations.render()





 