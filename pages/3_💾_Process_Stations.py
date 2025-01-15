import streamlit as st
from tabs import page3_tab1_process_stations, page3_tab2_visualize_datasets

tab1, tab2 = st.tabs(["Processar Estações", "Datasets CEDA"])

with tab1:
    page3_tab1_process_stations.render()

with tab2:
    page3_tab2_visualize_datasets.render()




 