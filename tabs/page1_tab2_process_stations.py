import streamlit as st
from utils.gsheets_connection import get_connection

def render():
    conn = get_connection()
    with st.container():
                st.subheader("Processar Estações")
        
                def load_infos_data():
                    return conn.read(worksheet="Infos")

                infos_data = load_infos_data()

                selected_infos_columns = ["Dataset", "Tipo", "Link"]
                infos_filtered = infos_data[selected_infos_columns]
                
                st.write("### Informações sobre o Dataset CEDA")
                st.dataframe(infos_filtered, use_container_width=True)

            