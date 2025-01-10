import streamlit as st
from tabs import page1_tab1_visualize_stations, page1_tab2_process_stations

st.title('Data Extract from CEDA')
st.subheader('Gustavo Machado - UNIFESSPA')
st.text('https://github.com/machadogustavo/ceda-streamlit')
st.text('Versão: 1.0.0')

tab1, tab2 = st.tabs(["Tabela de Estações","Processar Estações"])

with tab1:
    page1_tab1_visualize_stations.render()

with tab2:
    page1_tab2_process_stations.render()





 