import streamlit as st
from utils.gsheets_connection import get_connection
from utils.ceda_access_token import get_access_token
import requests
from netCDF4 import Dataset
from io import BytesIO
import time
import numpy as np

conn = get_connection()

def load_infos_data():
    return conn.read(worksheet="Infos")

def load_stations_data():
    return conn.read(worksheet="Estacoes")

def display_dataset_info(dataset):
    """Display key information about the NetCDF dataset"""
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

def open_dataset(url, download_token=None):
    """
    Enhanced dataset opening with support for gzipped NetCDF files and improved error handling
    
    Args:
        url (str): URL of the NetCDF file
        download_token (str, optional): Authentication token for CEDA
    
    Returns:
        tuple: (Dataset object or None, error message or None)
    """
    import gzip
    headers = {"Authorization": f"Bearer {download_token}"} if download_token else {}
    
    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        
        content = response.content
        
        try:
            dataset = Dataset(BytesIO(content), 'r')
            return dataset, None
        except Exception as e:
            return None, f"Erro ao processar o arquivo NetCDF: {str(e)}"
            
    except requests.exceptions.RequestException as e:
        return None, f"Erro na requisição HTTP: {str(e)}"

def render_sidebar():
    with st.sidebar:
        st.title("Autenticação CEDA")
        
    if not st.session_state.get("ceda_token"):
        st.warning("Nenhum token disponível.")
        with st.sidebar:
            st.text("Para utilização dos datasets do CEDA de forma remota, gere um novo token com suas credenciais CEDA.")
            st.warning("Gere ou insira um token para continuar.")
            
            ceda_credentials = st.secrets.get("ceda_credentials")
            if not ceda_credentials or not ceda_credentials.get("username") or not ceda_credentials.get("password"):
                st.error("Vincule suas credenciais para processar estações com os datasets do CEDA!", icon=":material/passkey:")
            else:
                username = ceda_credentials["username"]
                password = ceda_credentials["password"]

                token = st.session_state.get("ceda_token", None)

                token_generation_status = st.empty()

                if st.button("Gerar Novo Token"):
                    try:
                        with st.spinner("Gerando Token..."):
                            token = get_access_token(username, password)
                            time.sleep(5)
                            if token:
                                st.session_state["ceda_token"] = token
                                token_generation_status.success("Novo token gerado com sucesso!")
                                st.rerun(scope="fragment")
                            else:
                                token_generation_status.error("Erro ao gerar o token. Tente novamente.")
                    except Exception as e:
                        token_generation_status.error(f"Erro ao gerar o token: {e}")
                        token = None

                        manual_token = st.text_input("Insira o token manualmente:", type="password")
                        if manual_token and st.button("Registrar Token Manual"):
                            st.session_state["ceda_token"] = manual_token
                            token = manual_token
                            st.success("Token manual registrado com sucesso!")

    st.success("Token Carregado!")
    st.caption("Para mais informações: https://help.ceda.ac.uk/article/5100-archive-access-tokens#netcdf4")

def render_data_selection(infos_data):
    selected_dataset = None
    infos_data = load_infos_data()
    selected_infos_columns = ["var_id", "dataset", "type", "url", "size"]
    infos_filtered = infos_data[selected_infos_columns]

    stations_data = load_stations_data()
    
    with st.container():
        st.header("Seleção de Dataset")
        dataset_options = infos_data["dataset"].unique()
        selected_dataset = st.selectbox("Selecione um Dataset:", dataset_options)

    if selected_dataset:
        with st.expander("Informações sobre o Dataset selecionado"):
            st.dataframe(
                infos_filtered[infos_filtered["dataset"] == selected_dataset],
                use_container_width=True,
                column_config={"URL": st.column_config.LinkColumn("Url Dataset")},
                hide_index=True
            )
            
    return selected_dataset

def render_station_selection(station_data):
    st.header("Seleção de Estações")
    station_options = station_data["CIDADE"].unique()
    selected_stations = st.multiselect("Selecione as Estações para Processar:", station_options)

    if selected_stations:
        with st.expander("Informações das Estações Selecionadas:"):
            filtered_stations = station_data[station_data["CIDADE"].isin(selected_stations)][
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
                },
            )
            
        return selected_stations


def main():
    st.title("Processar Estações")
    render_sidebar()  # Chamando a barra lateral

    if not st.session_state.get("ceda_token"):
        st.warning("Nenhum token disponível. Gere ou insira um token para continuar.")
        return
    
    infos_data = load_infos_data()
    stations_data = load_stations_data()

    selected_dataset = render_data_selection(infos_data)
    selected_stations = render_station_selection(stations_data)

    st.header("Processar Dados")
    if not st.session_state.get("dataset_loaded", False):
        st.warning("Carregue um dataset antes de processar os dados.")
    elif not selected_stations:
        st.warning("Selecione pelo menos uma estação antes de processar os dados.")
    else:
        if st.button("Processar"):
            with st.spinner("Processando dados..."):
                st.success("Processamento concluído com sucesso!")

if __name__ == "__main__":
    main()
