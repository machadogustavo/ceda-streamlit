import streamlit as st
from utils.gsheets_connection import get_connection
from utils.ceda_access_token import get_access_token
import requests
from netCDF4 import Dataset
from io import BytesIO
import numpy as np

conn = get_connection()

def load_infos_data():
    return conn.read(worksheet="Infos")

def load_stations_data():
    return conn.read(worksheet="Estacoes")

def display_dataset_info(dataset):
    st.subheader("Informações do Dataset")
    
    st.write("**Dimensões:**")
    for dim_name, dim in dataset.dimensions.items():
        st.write(f"- {dim_name}: {len(dim)}")

    st.write("**Variáveis:**")
    for var_name, var in dataset.variables.items():
        st.write(f"- {var_name}")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"  - Dimensões: {var.dimensions}")
        with col2:
            st.write(f"  - Tipo: {var.dtype}")
    
    if dataset.ncattrs():
        st.write("**Atributos Globais:**")
        for attr in dataset.ncattrs():
            value = dataset.getncattr(attr)
            if isinstance(value, (str, int, float, np.integer, np.floating)):
                st.write(f"- {attr}: {value}")

def render():
    st.title("Processar Estações")
    
    with st.sidebar:
        st.title("Autenticação CEDA")
        
        ceda_credentials = st.secrets.get("ceda_credentials")
        token = st.session_state.get("ceda_token")
        
        if not token:
            st.text("Para utilização dos datasets do CEDA de forma remota, gere um novo token com suas credenciais CEDA.")
            st.warning("Gere um token para continuar.")
            
            if not ceda_credentials or not ceda_credentials.get("username") or not ceda_credentials.get("password"):
                st.error("Vincule suas credenciais para processar estações com os datasets do CEDA!", icon=":material/passkey:")
            else:
                username = ceda_credentials["username"]
                password = ceda_credentials["password"]

                token_generation_status = st.empty()

                if st.button("Gerar Novo Token"):
                    try:
                        with st.spinner("Gerando Token..."):
                            new_token = get_access_token(username, password)
                            if new_token:
                                st.session_state["ceda_token"] = new_token
                                token_generation_status.success("Token gerado!")
                                st.rerun()
                            else:
                                token_generation_status.error("Erro ao gerar token.")
                    except Exception as e:
                        token_generation_status.error(f"Erro ao gerar Token!")
                        print(f"Erro ao gerar token: {str(e)}")
                        
                        st.caption("Tente inserir manulmente um token")
                        
                        manual_token = st.text_input("Token Manual:", type="password")
                        if manual_token and st.button("Registrar Token"):
                            st.session_state["ceda_token"] = manual_token
                            st.rerun()
            

              
        else:
            st.success("Token Ativo ✓")
            if st.button("Limpar Token"):
                del st.session_state["ceda_token"]
                st.rerun()
    
    if st.session_state.get("ceda_token"):
        infos_data = load_infos_data()
        stations_data = load_stations_data()

        st.header("Seleção de Dataset")
        dataset_options = infos_data["dataset"].unique()
        selected_dataset = st.selectbox("Selecione um Dataset:", dataset_options)

        if selected_dataset:
            selected_infos_columns = ["var_id", "dataset", "type", "url", "size"]
            dataset_info = infos_data[infos_data["dataset"] == selected_dataset][selected_infos_columns]
            
            with st.expander("Informações sobre o Dataset selecionado"):
                st.dataframe(
                    dataset_info,
                    use_container_width=True,
                    column_config={"URL": st.column_config.LinkColumn("Url Dataset")},
                    hide_index=True
                )

            st.header("Seleção de Estações")
            station_options = stations_data["CIDADE"].unique()
            selected_stations = st.multiselect("Selecione as Estações para Processar:", station_options)

            if selected_stations:
                with st.expander("Informações das Estações Selecionadas:"):
                    filtered_stations = stations_data[stations_data["CIDADE"].isin(selected_stations)][
                        ["CD_ESTACAO", "CIDADE", "SG_ESTADO", "VL_LATITUDE", "VL_LONGITUDE", "CD_SITUACAO"]
                    ]

                    display_columns = {
                        "CD_ESTACAO": "Código da Estação",
                        "CIDADE": "Cidade",
                        "SG_ESTADO": "Estado",
                        "VL_LATITUDE": "Latitude",
                        "VL_LONGITUDE": "Longitude",
                        "CD_SITUACAO": "Situação"
                    }
                    
                    st.dataframe(
                        filtered_stations.rename(columns=display_columns),
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Código da Estação": st.column_config.NumberColumn(format="%d"),
                            "Latitude": st.column_config.NumberColumn(format="%d"),
                            "Longitude": st.column_config.NumberColumn(format="%d"),
                            "Situação": st.column_config.TextColumn()
                        }
                    )

                st.header("Processar Dados")
                if st.button("Processar Dataset"):
                    with st.spinner("Carregando dataset..."):
                        try:
                            dataset_url = dataset_info.iloc[0]["url"]
                            headers = {"Authorization": f"Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI4ZjhmaUpyaUtDY3hmaHhzdU5vazVEekdJdFZ4amhhTWNJa05ZX2U4MnhJIn0.eyJleHAiOjE3MzcxNTExNTgsImlhdCI6MTczNjg5MTk1OCwianRpIjoiZTAxZWM4M2EtNTg3OS00MTY4LTg1YzUtMDUzOTc1ZjdlYTcwIiwiaXNzIjoiaHR0cHM6Ly9hY2NvdW50cy5jZWRhLmFjLnVrL3JlYWxtcy9jZWRhIiwic3ViIjoiODAxZjY5YTEtYzExYy00MDIyLTliY2YtNzQ3MGNiNGRkMmVhIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoic2VydmljZXMtcG9ydGFsLWNlZGEtYWMtdWsiLCJzZXNzaW9uX3N0YXRlIjoiYzIwMmE1YzEtNmU5MS00MDhmLWIxNmEtNDZmODNiZjNkNDhiIiwiYWNyIjoiMSIsInNjb3BlIjoiZW1haWwgb3BlbmlkIHByb2ZpbGUgZ3JvdXBfbWVtYmVyc2hpcCIsInNpZCI6ImMyMDJhNWMxLTZlOTEtNDA4Zi1iMTZhLTQ2ZjgzYmYzZDQ4YiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJvcGVuaWQiOiJodHRwczovL2NlZGEuYWMudWsvb3BlbmlkL0d1c3Rhdm8uTWFjaGFkbyIsIm5hbWUiOiJHdXN0YXZvIE1hY2hhZG8iLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJnbXVuaWZlc3NwYSIsImdpdmVuX25hbWUiOiJHdXN0YXZvIiwiZmFtaWx5X25hbWUiOiJNYWNoYWRvIiwiZW1haWwiOiJndXN0YXZvLnBhaXhhb0B1bmlmZXNzcGEuZWR1LmJyIn0.a6qh9RuLgJiSOCK-c7gKRwlJTwsTPlm1qydcfkhDB0Ez63_HwOiSz3sSoSnw-cazellUTUGOoLIazq4QsjGg83TlFKn5o1EniKbxD04a6tqZTMY8JcylCwoLZ17KL8Weu-QBJFY8DFqhAbN6AjtXeTBnu62bgXNLAfS3f_ojR0vHABRlFB2hcRZhF5cja5pXaZ1EYJOmLsCrIw5acVQy7fW8lTJVqjUI9qnMLrL6j5V_bV2rhyUNgjWoSv7ENdUqM1rcgc0oCiuaeiQ-KkZ6tjZyHEsNe-uVhEKfupJ0hdnO6OAlNXo-zyJB3Qi6HaN7OzXcgDn78VR8_mUvdpoH_A"}
                            
                            with st.spinner("Fazendo requisição do dataset..."):
                                response = requests.get(dataset_url, headers=headers, stream=True)
                                st.info(f"Status da requisição: {response.status_code}")
                                st.info(f"Content-Type: {response.headers.get('content-type', 'Não especificado')}")
                                st.info(f"Content-Length: {response.headers.get('content-length', 'Não especificado')}")
                                
                                print(response.content)
                                
                                st.html(response.content)
                                
                             
                                response.raise_for_status()
                                
                               
                                content_start = response.content[:50]
                                st.info(f"Primeiros bytes do conteúdo (hex): {content_start.hex()}")
                                
         
                                import tempfile
                                import os
                                
                                with tempfile.NamedTemporaryFile(suffix='.nc', delete=False, mode='wb') as tmp_file:
                                  
                                    tmp_file.write(response.content)
                                    tmp_file_path = tmp_file.name
                                    
                                    st.info(f"Arquivo temporário criado em: {tmp_file_path}")
                                    st.info(f"Tamanho do arquivo: {os.path.getsize(tmp_file_path)} bytes")
                                
                                try:
                                   
                                    import xarray as xr
                                    try:
                                        ds = xr.open_dataset(tmp_file_path)
                                        st.success("Arquivo aberto com sucesso usando xarray!")
                                        st.write(ds)
                                    except Exception as xr_error:
                                        st.warning(f"Erro ao abrir com xarray: {str(xr_error)}")
                                    
                                    
                                    dataset = Dataset(tmp_file_path, 'r')
                                    
                                    st.subheader("Informações Básicas do Dataset")
                                    st.write(f"Número de variáveis: {len(dataset.variables)}")
                                    st.write(f"Número de dimensões: {len(dataset.dimensions)}")
                                    
                                    st.subheader("Primeiras Variáveis")
                                    for i, (var_name, var) in enumerate(dataset.variables.items()):
                                        if i < 5:
                                            st.write(f"\n**{var_name}**")
                                            st.write(f"- Dimensões: {var.dimensions}")
                                            st.write(f"- Tipo: {var.dtype}")
                                            
                                            try:
                                                data = var[:]
                                                if data.size > 0:
                                                    st.write("- Primeiros valores:")
                                                    st.write(data.flatten()[:5])
                                            except Exception as e:
                                                st.write(f"- Não foi possível mostrar valores: {str(e)}")
                                    
                                    dataset.close()
                                    
                                finally:
               
                                    if os.path.exists(tmp_file_path):
                                        try:
                                            os.unlink(tmp_file_path)
                                            st.info("Arquivo temporário removido com sucesso")
                                        except Exception as e:
                                            st.warning(f"Erro ao remover arquivo temporário: {str(e)}")

                        except requests.exceptions.RequestException as e:
                            st.error(f"Erro na requisição HTTP: {str(e)}")
                            if hasattr(e, 'response'):
                                st.error(f"Resposta do servidor: {e.response.text}")
                        except Exception as e:
                            st.error(f"Erro ao carregar o dataset: {str(e)}")
                        
                        st.write("---")
                        st.write("Informações de Debug:")
                        st.write(f"URL do dataset: {dataset_url}")
                        st.write(f"Headers da requisição: {headers}")
            else:
                st.warning("Selecione pelo menos uma estação antes de processar os dados.")
    else:
        st.info("Por favor, gere ou insira um token na barra lateral para começar.")

if __name__ == "__main__":
    render()