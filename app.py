import streamlit as st
from streamlit_gsheets import GSheetsConnection
from st_files_connection import FilesConnection
from streamlit_autorefresh import st_autorefresh

import numpy as np
import os
import time as tm
import random
import base64
import pandas as pd
import json

conn = st.connection("gsheets", type=GSheetsConnection)

st.title('Data Extract from CEDA')
st.subheader('Gustavo Machado - UNIFESSPA')


tab1, tab2, tab3 = st.tabs(["Processar Estações", "Visualizar Dados CEDA/Inmet", "Comparativo KGE"])
 
with tab1:
      
    st.subheader("Tabela de Dados - Estações")
    
    
    col1, col2 = st.columns(2)
    
    with col1:
        # @st.cache_data
        def load_stations_data():
            df_stations = conn.read()
            return df_stations
        
        data_load_state = st.text('Carregando Estações...')
        data = load_stations_data()
        data_load_state.empty()
        
        selected_columns = ["DC_NOME", "CIDADE", "SG_ESTADO", "VL_LATITUDE", "VL_LONGITUDE", "BIOMA"]
        data_filtered = data[selected_columns]

        edit_mode = st.checkbox("Ativar modo de edição")
        
        if edit_mode:
            edited_data = st.data_editor(data_filtered, num_rows="dynamic")

            if st.button("Salvar Alterações"):
                conn.update(worksheet="Estacoes",data=edited_data)
                st.success("Alterações salvas com sucesso!")
                st.rerun()
        else:
            st.dataframe(data_filtered)


    

    with col2:
        st.text("Adicionar Nova Estação")
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
                conn.update(worksheet="Estacoes",data=updated_data)
                
                st.success("Nova estação adicionada com sucesso!")
                st.rerun()



    
    
with tab2:
    st.write(data)
    
with tab3:
    st.write("tchau")










