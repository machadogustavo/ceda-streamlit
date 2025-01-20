import streamlit as st
import pydeck as pdk
import pandas as pd
from utils.gsheets_connection import get_connection

def convert_coordinates(coord_str):
    try:
        num = float(coord_str)
        return num / 100000000
    except ValueError:
        return None

def render():

    st.title("Estações Meteorológicas INMET")    
    
    conn = get_connection()
    
    def load_stations_data():
        df = conn.read(worksheet="Estacoes")
        
        df['lat'] = df['VL_LATITUDE'].apply(convert_coordinates)
        df['lon'] = df['VL_LONGITUDE'].apply(convert_coordinates)
        
        return df
    
    df = load_stations_data()
    
    cont1 = st.container()
    cont2 = st.container()
    cont3 = st.container()

    with st.expander("Filtros", icon=":material/filter_alt:"):
        

        estados = sorted(df['SG_ESTADO'].unique())
        selected_estados = st.multiselect(
            'Selecione os Estados:',
            estados,
            default=['PA']
        )
      
    
        estacoes_disponiveis = sorted(df['DC_NOME'].unique())

        estacoes_disponiveis = sorted(df[df['SG_ESTADO'].isin(selected_estados)]['DC_NOME'].unique())
        selected_estacoes = st.multiselect(
            'Selecione as Estações:',
            estacoes_disponiveis,
            default=[]
        )

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
        'Latitude': filtered_df['lat'],
        'Longitude': filtered_df['lon'],
        'Estação': filtered_df['DC_NOME'] + ' (Código: ' + filtered_df['CD_ESTACAO'].astype(str) + ')'
    }).dropna()

    brazil_lat = -14.235
    brazil_lon = -51.9253

    point_layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_data,
        get_position=["Longitude", "Latitude"],
        get_color="[200, 30, 0, 160]",
        get_radius=50000,
        pickable=True
    )

    view_state = pdk.ViewState(
        latitude=brazil_lat,
        longitude=brazil_lon,
        zoom=3,
        pitch=50
    )

    chart = pdk.Deck(
        layers=[point_layer],
        initial_view_state=view_state,
        tooltip={"html": "<b>Estação:</b> {Estação}"},
    )

    with st.container():
        col1, col2, col3 = st.columns(3, gap="large")

        with col1:
            st.metric("Total de Estações", len(filtered_df))
        with col2:
            estados_count = filtered_df['SG_ESTADO'].value_counts()
            st.metric("Estados", len(estados_count))
        with col3:
            operantes = len(filtered_df[filtered_df['CD_SITUACAO'] == 'Operante'])
            st.metric("Estações Operantes", operantes)

        if not map_data.empty:
            st.pydeck_chart(chart, use_container_width=True)
        else:
            st.error("Não há coordenadas válidas para exibir no mapa")

if __name__ == "__main__":
    render()