import streamlit as st
from utils.gsheets_connection import get_connection

conn = get_connection()


def convert_df_to_csv(df):
    """Converte DataFrame para CSV"""
    return df.to_csv(index=False).encode('utf-8')



def render():
    with st.container():
        st.title("Dataset INMET - Captação Mensal")
        with st.container():
            @st.cache_data
            def load_stations_data():
                return conn.read(worksheet="Dados INMET")
            data = load_stations_data()
            st.dataframe(data, use_container_width=True)
            
            
    csv = convert_df_to_csv(data)
    st.download_button(
        label="Download Dataset .CSV",
        data=csv,
        file_name='dados_inmet_1961-01-31_2025-01-01.csv',
        mime='text/csv'
    )
       