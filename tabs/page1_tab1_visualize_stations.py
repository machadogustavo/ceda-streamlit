import streamlit as st
import pandas as pd
from utils.gsheets_connection import get_connection

def render():
    conn = get_connection()

    with st.container():
        st.subheader("Tabela de Dados - Estações")

        with st.container():
            def load_stations_data():
                return conn.read()

            data = load_stations_data()
            selected_columns = ["DC_NOME", "CIDADE", "SG_ESTADO", "VL_LATITUDE", "VL_LONGITUDE", "BIOMA"]
            data_filtered = data[selected_columns]

            edit_mode = st.toggle("Ativar modo de edição", key="edit_mode_toggle")

            if edit_mode:
                edited_data = st.data_editor(data_filtered, num_rows="dynamic")
                if st.button("Salvar Alterações"):
                    conn.update(worksheet="Estacoes", data=edited_data)
                    st.success("Alterações salvas com sucesso!")
                    st.rerun()
            else:
                st.dataframe(data_filtered, use_container_width=True)
                
    with st.container():
        with st.expander("Adicionar Nova Estação"):
            with st.form("add_station_form"):
                dc_nome = st.text_input("Nome da Estação (DC_NOME)")
                cidade = st.text_input("Cidade")
                sg_estado = st.text_input("Estado (SG_ESTADO)")
                vl_latitude = st.number_input("Latitude", format="%.6f")
                vl_longitude = st.number_input("Longitude", format="%.6f")
                bioma = st.text_input("Bioma")

                submitted = st.form_submit_button("Adicionar Estação")

                if submitted:
                    new_row = pd.DataFrame([{
                        "DC_NOME": dc_nome,
                        "CIDADE": cidade,
                        "SG_ESTADO": sg_estado,
                        "VL_LATITUDE": vl_latitude,
                        "VL_LONGITUDE": vl_longitude,
                        "BIOMA": bioma,
                    }])
                    updated_data = pd.concat([data, new_row], ignore_index=True)
                    conn.clear()
                    conn.update(worksheet="Estacoes", data=updated_data)

                    st.success("Nova estação adicionada com sucesso!")
                    st.rerun()

