import streamlit as st
import pandas as pd
from utils.gsheets_connection import get_connection

conn = get_connection()

def load_and_prepare_data():
    """Carrega e prepara os dados do Google Sheets"""
    df = conn.read(worksheet="Dados INMET")
    df['Data_Medicao'] = pd.to_datetime(df['Data_Medicao'])
    return df

def convert_df_to_csv(df):
    """Converte DataFrame para CSV"""
    return df.to_csv(index=False).encode('utf-8')


def render():
    st.title("Dashboard de Dados INMET")
    
    df = load_and_prepare_data()
    
    with st.expander("Filtros", icon=":material/filter_alt:"):
        cont1 = st.container()
        cont2 = st.container()

        with cont1:
            col1, col2 = st.columns(2)
            all_stations = sorted(df['Nome'].unique())

            # cont1 = st.container()
            
            # with cont1:
            #     with col1: 
            #         mark_all = st.button("Marcar Todas")
                
            #     with col2: 
            #         unmark_all = st.button("Desmarcar Todas")

            # if mark_all:
            #     selected_stations = all_stations
            # elif unmark_all:
            #     selected_stations = []
            # else:
            selected_stations = []

            selected_stations = st.multiselect(
                "Estações",
                options=all_stations,
                default=selected_stations,
                placeholder="Selecione uma ou mais estações"
            )

        with cont2:
            col1, col2, col3 = st.columns(3)

            with col1:
                max_date = df['Data_Medicao'].max().date()
                end_date = st.date_input("Data Final", max_date)

            with col2:
                min_date = df['Data_Medicao'].min().date()
                start_date = st.date_input("Data Inicial", min_date)

            with col3:
                variables = {
                    'PRECIPITACAO_TOTAL_MENSAL_mm': 'Precipitação Total (mm)',
                    'TEMPERATURA_MEDIA_COMPENSADA_MENSAL_C': 'Temperatura Média (°C)',
                    'VENTO_VELOCIDADE_MEDIA_MENSAL_m/s': 'Velocidade do Vento (m/s)',
                }
                selected_var = st.selectbox(
                    "Variável para Análise",
                    options=list(variables.keys()),
                    format_func=lambda x: variables[x]
                )

            
    mask = (
        (df['Nome'].isin(selected_stations)) &
        (df['Data_Medicao'].dt.date >= start_date) &
        (df['Data_Medicao'].dt.date <= end_date)
    )
    filtered_df = df[mask]
    
    if not selected_stations:
        st.warning("⚠️ Por favor, selecione pelo menos uma estação!")
        return
             
    if filtered_df.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        return
    
    st.subheader(f"Série Temporal - {variables[selected_var]}")
    
    chart_data = filtered_df.pivot(
        index='Data_Medicao',
        columns='Nome',
        values=selected_var
    )
    
    st.line_chart(chart_data)
        
    csv = convert_df_to_csv(filtered_df)
    

    st.download_button(
        type="secondary",
        label="Download .CSV",
        data=csv,
        file_name=f'dados_inmet_{start_date}_{end_date}.csv',
        mime='text/csv',
        icon=":material/description:"
    )
    

    st.text(f"{variables[selected_var]}")
    stats_df = filtered_df.groupby('Nome')[selected_var].agg([
            ('Média', 'mean'),
            ('Mínimo', 'min'),
            ('Máximo', 'max'),
            ('Desvio Padrão', 'std')
        ]).round(2)
    st.dataframe(stats_df, use_container_width=True)
    

    with st.expander("Visualizar Dataset Filtrado"):
        st.dataframe(
            filtered_df.sort_values(['Nome', 'Data_Medicao']),
            use_container_width=True,hide_index=True
        )

if __name__ == "__main__":
    render()