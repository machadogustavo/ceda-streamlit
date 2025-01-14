import streamlit as st
from utils.gsheets_connection import get_connection
from utils.ceda_access_token import get_access_token
import requests

conn = get_connection()

st.title("Processar Estações")

def load_infos_data():
    return conn.read(worksheet="Infos")

def load_stations_data():
    return conn.read(worksheet="Estacoes")

with st.sidebar:
    st.title("Autenticação CEDA")
    st.text("Para utilização dos datasets do CEDA de forma remota, gere um novo token com suas credenciais CEDA.")
    
    ceda_credentials = st.secrets.get("ceda_credentials")
    if not ceda_credentials or not ceda_credentials.get("username") or not ceda_credentials.get("password"):
        st.error("Vincule suas credenciais para processar estações com os datasets do CEDA!", icon=":material/passkey:")
    else:
        username = ceda_credentials["username"]
        password = ceda_credentials["password"]

        token = st.session_state.get("ceda_token", None)

        token_generation_status = st.empty()  # Para exibir mensagens temporárias

        if st.button("Gerar Novo Token"):
            try:
                token = get_access_token(username, password)
                if token:
                    st.session_state["ceda_token"] = token
                    token_generation_status.success("Novo token gerado com sucesso!")
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



            
                
        st.caption("Para mais informações: https://help.ceda.ac.uk/article/5100-archive-access-tokens#netcdf4")

if not token:
    st.warning("Nenhum token disponível. Gere ou insira um token para continuar.")
else:
    infos_data = load_infos_data()
    selected_infos_columns = ["Dataset", "Tipo", "Link"]
    infos_filtered = infos_data[selected_infos_columns]

    stations_data = load_stations_data()

    # @st.cache_data
    def open_dataset(url, download_token=None):
        headers = {"Authorization": f"Bearer {download_token}"} if download_token else {}
        response = requests.get(url, headers=headers, stream=True)

        if response.status_code == 200:
            st.toast(f"Dataset carregado com sucesso da URL: {url}")
            return response.content
        else:
            st.error(f"Erro ao carregar o dataset. Status: {response.status_code}")
            return None

    with st.container():
        st.header("Seleção de Dataset")
        dataset_options = infos_data["Dataset"].unique()
        selected_dataset = st.selectbox("Selecione um Dataset:", dataset_options)

        if selected_dataset:
            with st.expander("Informações sobre o Dataset selecionado"):
                st.dataframe(
                    infos_filtered[infos_filtered["Dataset"] == selected_dataset],
                    use_container_width=True,
                    column_config={"Link": st.column_config.LinkColumn("Link Dataset")},
                    hide_index=True
                )

            if st.button("Carregar Dataset"):
                if token:
                    dataset_url = infos_data[infos_data["Dataset"] == selected_dataset]["Link"].values[0]
                    with st.spinner("Carregando o dataset..."):
                        dataset_content = open_dataset(dataset_url, download_token=token)
                        if dataset_content:
                            st.success(f"Dataset '{selected_dataset}' carregado com sucesso. Pronto para seleção de estações.")
                            st.session_state["dataset_loaded"] = True
                else:
                    st.warning("Nenhum token disponível. Insira manualmente ou gere um novo para continuar.")
        else:
            st.info("Selecione um dataset para continuar.")

    with st.container():
        st.header("Seleção de Estações")
        if not st.session_state.get("dataset_loaded", False):
            st.info("Carregue um dataset antes de selecionar as estações.")
        else:
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
                        },
                    )


            else:
                st.info("Selecione pelo menos uma estação para habilitar o processamento.")

    with st.container():
        st.header("Processar Dados")
        if not st.session_state.get("dataset_loaded", False):
            st.warning("Carregue um dataset antes de processar os dados.")
        elif not selected_stations:
            st.warning("Selecione pelo menos uma estação antes de processar os dados.")
        else:
            if st.button("Processar"):
                with st.spinner("Processando dados..."):

                    st.success("Processamento concluído com sucesso!")
