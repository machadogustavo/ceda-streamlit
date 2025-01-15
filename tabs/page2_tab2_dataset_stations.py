import streamlit as st
import pandas as pd
import time
from utils.gsheets_connection import get_connection

conn = get_connection()

def load_stations_data():
    """Função para carregar os dados das estações."""
    return conn.read()

@st.dialog("Adicionar Nova Estação", width="large")
def new_station_dialog(data, display_columns, conn):
    """Dialog para adicionar uma nova estação."""
    with st.form("add_station_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            cd_estacao = st.text_input("Código Estação")
            cidade = st.text_input("Cidade")
            sg_estado = st.text_input("Estado", max_chars=2)

        with col2:
            vl_latitude = st.number_input("Latitude", format="%.6f")
            vl_longitude = st.number_input("Longitude", format="%.6f")

        with col3:
            bioma = st.text_input("Bioma")
            situacao = st.selectbox("Situação", ("Operante",))

        submitted = st.form_submit_button("Adicionar Estação")

        if submitted:
            with st.spinner("Adicionando nova estação..."):
                try:

                    new_row = pd.DataFrame([{
                        "CD_ESTACAO": cd_estacao,
                        "DC_NOME": cidade.upper(),
                        "CIDADE": cidade,
                        "SG_ESTADO": sg_estado,
                        "VL_LATITUDE": vl_latitude,
                        "VL_LONGITUDE": vl_longitude,
                        "BIOMA": bioma,
                        "CD_SITUACAO": situacao
                    }])

                    updated_data = pd.concat([data[list(display_columns.keys())], new_row], ignore_index=True)
                    conn.clear()
                    conn.update(worksheet="Estacoes", data=updated_data)

                    st.toast("Nova estação adicionada com sucesso!", icon="✅")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao adicionar estação: {e}")

def render():
    """Função principal para renderizar a aplicação."""
    data = load_stations_data()
    display_columns = {
        "CD_ESTACAO": "Código da Estação",
        "CIDADE": "Cidade",
        "SG_ESTADO": "Estado",
        "VL_LATITUDE": "Latitude",
        "VL_LONGITUDE": "Longitude",
        "BIOMA": "Bioma",
    }

    data_filtered = data[list(display_columns.keys())].rename(columns=display_columns)

    st.subheader("Tabela de Dados - Estações")
    st.dataframe(data_filtered, use_container_width=True)
    
    if st.button("Nova Estação", type="secondary"):
        new_station_dialog(data, display_columns, conn)


if __name__ == "__main__":
    render()
