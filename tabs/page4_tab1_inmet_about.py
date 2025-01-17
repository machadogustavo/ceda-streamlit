import streamlit as st
from utils.gsheets_connection import get_connection

conn = get_connection()

def render():
    def load_stations_data():
        return conn.read(worksheet="Dados INMET")
    
    data = load_stations_data()
    
    measurement_keywords = ["TEMPERATURA", "PRECIPITACAO", "VENTO"]
    
    measurement_columns = [col for col in data.columns if any(keyword in col.upper() for keyword in measurement_keywords)]
    
    unique_stations = data['Estacao'].nunique()

    st.title("Dados INMET")
    
    with st.container(border=True):
        col1, col2, col3 = st.columns(3, gap="small", vertical_alignment="center")
    
        with col1: 
            st.metric("Estações", unique_stations)
        with col2:
            st.metric("Data de Filtragem", "1961 - 2025")
        with col3:
            st.metric("Dados Filtrados", len(data))

        st.subheader("Variáveis Disponíveis")
        for column in measurement_columns:
            mean_value = data[column].mean()
            
            st.markdown(f"`{column}` - Média: {mean_value:.2f}")
        
    st.divider()
    
    with st.container():
        st.caption("Para mais informações sobre os dados acesse:")
        st.write("🌐 INMET: https://bdmep.inmet.gov.br/")
