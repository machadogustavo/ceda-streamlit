import streamlit as st
from utils.gsheets_connection import get_connection

conn = get_connection()

def render():
    def load_stations_data():
        return conn.read(worksheet="Dados INMET")
    
    data = load_stations_data()

    unique_stations = data['Estacao'].nunique()

    st.title("Dados INMET")
    st.write(f"{unique_stations} Estações | 1961-01-31 - 2025-01-01")
    st.markdown("- Precipitação Total (mm)")
    st.markdown("- Temperatura Média Condensada (c°)")
    st.markdown("- Vento Velocidade Média (m/s)")
    st.write("Disponível em: https://bdmep.inmet.gov.br/")
