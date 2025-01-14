import streamlit as st
import requests
from datetime import datetime, timezone, timedelta
from base64 import b64encode

TOKEN_KEY = "ceda_token"
TOKEN_URL = "https://services-beta.ceda.ac.uk/api/token/create/"


def load_cached_token():
    if TOKEN_KEY in st.session_state:
        token_data = st.session_state[TOKEN_KEY]

        if isinstance(token_data, dict):
            expires = token_data.get("expires")
            if expires:
                expires = datetime.fromisoformat(expires)
                if datetime.now(timezone.utc) < expires:
                    return token_data.get("access_token")
        else:
            st.error("Invalid token format. Expected a dictionary.")
    return None


def save_token_in_session(token, expires):
    st.session_state[TOKEN_KEY] = {"access_token": token, "expires": expires.isoformat()}


def generate_token(username, password):
    encoded_credentials = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    headers = {"Authorization": f"Basic {encoded_credentials}"}

    try:
        response = requests.post(TOKEN_URL, headers=headers)
        response.raise_for_status()

        data = response.json()
        token = data.get("access_token")
        expires_in = data.get("expires_in")

        if not token or not expires_in:
            raise ValueError("Erro ao gerar o token: Resposta inválida do servidor. Token ou tempo de expiração ausente.")

        expires = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        save_token_in_session(token, expires)
        return token

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Erro ao gerar o token: Erro na requisição ao servidor: {e}")

    except ValueError as e:
        raise ValueError(str(e))


def get_access_token(username, password):
    try:
        token = load_cached_token()
        if not token:
            token = generate_token(username, password)
        return token
    except ValueError as e:
        return str(e)
