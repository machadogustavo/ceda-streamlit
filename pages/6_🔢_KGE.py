import streamlit as st
from tabs import page6_tab1_kge_about, page6_tab2_process_kge

tab1, tab2 = st.tabs(["Sobre KGE", "Comparar Dados"])

with tab1:
    page6_tab1_kge_about.render()

with tab2:
    page6_tab2_process_kge.render()




 