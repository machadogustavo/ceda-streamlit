import streamlit as st
from tabs import page2_tab1_visualize_stations, page2_tab2_dataset_stations

tab1, tab2 = st.tabs(["Visualizar Estações", "Tabela de Estações"])

with tab1:
    page2_tab1_visualize_stations.render()

with tab2:
    page2_tab2_dataset_stations.render()




 