import streamlit as st
import pandas as pd
from utils.gsheets_connection import get_connection

def convert_coordinates(coord_str):
    try:
        num = float(coord_str)
        return num / 100000000
    except ValueError:
        return None

def render():
    st.title("Visualização das Estações Meteorológicas INMET")
    
    conn = get_connection()
    
    def load_stations_data():
        df = conn.read(worksheet="Estacoes")
        
        df['lat'] = df['VL_LATITUDE'].apply(convert_coordinates)
        df['lon'] = df['VL_LONGITUDE'].apply(convert_coordinates)
        
        return df
    
    df = load_stations_data()
    
    with st.sidebar:
        st.header("Filtros")
        
        # Filtro de Estados
        estados = sorted(df['SG_ESTADO'].unique())
        selected_estados = st.multiselect(
            'Selecione os Estados:',
            estados,
            default=['PA']
        )
        
        # Filtro dinâmico de Estações baseado nos estados selecionados
        estacoes_disponiveis = sorted(df[df['SG_ESTADO'].isin(selected_estados)]['DC_NOME'].unique())
        selected_estacoes = st.multiselect(
            'Selecione as Estações:',
            estacoes_disponiveis,
            default=[]
        )
        
        # Filtro de Situações
        situacoes = sorted(df['CD_SITUACAO'].unique())
        selected_situacoes = st.multiselect(
            'Selecione a Situação:',
            situacoes,
            default=['Operante']
        )
        
    if not selected_estados:
        st.warning("⚠️ Por favor, selecione pelo menos um estado!")
        return
        
    if not selected_situacoes:
        st.warning("⚠️ Por favor, selecione pelo menos uma situação!")
        return
    

    mask = (
        (df['SG_ESTADO'].isin(selected_estados)) &
        (df['CD_SITUACAO'].isin(selected_situacoes))
    )
    
    if selected_estacoes:
        mask = mask & (df['DC_NOME'].isin(selected_estacoes))
    
    filtered_df = df[mask]

    map_data = pd.DataFrame({
        'lat': filtered_df['lat'],
        'lon': filtered_df['lon'],
        'Estação': filtered_df['DC_NOME'] + ' (Código: ' + filtered_df['CD_ESTACAO'].astype(str) + ')'
    }).dropna()
    
    brazil_lat = -14.235
    brazil_lon = -51.9253
    
    if not map_data.empty:
        st.map(
            map_data,
            zoom=3,
            size=200,
            latitude=brazil_lat,
            longitude=brazil_lon
        )
    else:
        st.error("Não há coordenadas válidas para exibir no mapa")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Estações", len(filtered_df))
    
    with col2:
        estados_count = filtered_df['SG_ESTADO'].value_counts()
        st.metric("Estados", len(estados_count))
    
    with col3:
        operantes = len(filtered_df[filtered_df['CD_SITUACAO'] == 'Operante'])
        st.metric("Estações Operantes", operantes)

if __name__ == "__main__":
    render()