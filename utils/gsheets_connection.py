import streamlit as st
from streamlit_gsheets import GSheetsConnection

def get_connection():
    return st.connection("gsheets", type=GSheetsConnection)
