import google.generativeai as genai
import streamlit as st

def configure_api_key():
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    except Exception as e:
        st.error(f"Erro ao configurar a API Key: {e}")
        st.info("Por favor, certifique-se de que sua GOOGLE_API_KEY está configurada corretamente nos Secrets do Streamlit Cloud.")
        st.stop()

def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text
