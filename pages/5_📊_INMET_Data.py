import streamlit as st
from tabs import page4_tab1_inmet_about, page4_tab2_visualize_inmet, page4_tab3_visualize_dataset

list_of_tabs = ["Sobre", "Dashboard", "Dataset"]

tabs = st.tabs(list_of_tabs)


with tabs[0]:
    page4_tab1_inmet_about.render()

with tabs[1]:
    page4_tab2_visualize_inmet.render()

with tabs[2]:
    page4_tab3_visualize_dataset.render()
