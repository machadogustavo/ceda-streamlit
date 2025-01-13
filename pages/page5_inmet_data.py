import streamlit as st
from tabs import page4_tab1_inmet_about, page4_tab2_visualize_dashboard,page4_tab3_visualize_dataset

tab1, tab2, tab3= st.tabs(["Sobre", "Dashboard","Dataset"])

with tab1:
    page4_tab1_inmet_about.render()

with tab2:
    page4_tab2_visualize_dashboard.render()
    
with tab3:
    page4_tab3_visualize_dataset.render()











