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
            
            display_columns = {
                "CD_ESTACAO": "Código da Estação",
                "CIDADE": "Cidade",
                "SG_ESTADO": "Estado",
                "VL_LATITUDE": "Latitude",
                "VL_LONGITUDE": "Longitude",
                "BIOMA": "Bioma"
            }
            
            data_filtered = data[list(display_columns.keys())]
            
            data_filtered = data_filtered.rename(columns=display_columns)
            
            edit_mode = st.toggle("Ativar modo de edição", key="edit_mode_toggle")
            
            if edit_mode:
                edited_data = st.data_editor(data_filtered, num_rows="dynamic", use_container_width=True)
                if st.button("Salvar Alterações"):
                    reverse_columns = {v: k for k, v in display_columns.items()}
                    edited_data_original = edited_data.rename(columns=reverse_columns)
                    conn.update(worksheet="Estacoes", data=edited_data_original)
                    st.success("Alterações salvas com sucesso!")
                    st.rerun()
            else:
                st.dataframe(data_filtered, use_container_width=True, hide_index=True, column_config={"Código da Estação": st.column_config.NumberColumn(format="%d"), "Latitude": st.column_config.NumberColumn(format="%d"), "Longitude": st.column_config.NumberColumn(format="%d")})
                
                csv = data_filtered.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Download Estações .CSV",
                    csv,
                    "estacoes.csv",
                    "text/csv",
                    key='download-csv'
                )
        
        with st.sidebar:
            with st.expander("Adicionar Nova Estação"):
                with st.form("add_station_form"):
                    dc_nome = st.text_input("Nome da Estação")
                    cidade = st.text_input("Cidade")
                    sg_estado = st.text_input("Estado", max_chars=2)
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
                        
                        updated_data = pd.concat([data[list(display_columns.keys())], new_row], ignore_index=True)
                        
                        conn.clear()
                        conn.update(worksheet="Estacoes", data=updated_data)
                        
                        st.success("Nova estação adicionada com sucesso!")
                        st.rerun()

if __name__ == "__main__":
    render()