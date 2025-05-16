import streamlit as st
from gemini_utility import get_gemini_response, configure_api_key # Esta linha precisa do gemini_utility.py

# Configura a API Key do Gemini usando st.secrets (boa prática de segurança)
configure_api_key()

# --- Configurações da Página ---
st.set_page_config(page_title="GATEBOT - Seu Assistente de IA", page_icon="🤖")

# --- CSS Personalizado para a Sidebar ---
st.markdown("""
<style>
    /* Estilo para a cor de fundo da sidebar. Você pode mudar o #262730 para outra cor. */
    .st-emotion-cache-nahz7x {
        background-color: #262730;
    }
    /* Estilo para o texto do sidebar. Você pode mudar a cor e o tamanho da fonte. */
    .st-emotion-cache-1pxazr6 {
        color: white;
    }
    /* Estilo para links ou elementos interativos na sidebar */
    .st-emotion-cache-1km1mho a {
        color: #8D8DFF; /* Um azul mais claro para links */
    }
</style>
""", unsafe_allow_html=True)


# --- Título e Imagem de Capa ---
st.title("GATEBOT")
st.header("Seu Assistente de IA com Google Gemini")

# A imagem de capa do GATEBOT, agora hospedada no GitHub e funcionando!
st.image("https://raw.githubusercontent.com/brun372/gatebot-online/main/B5w10V3.PNG", caption="Seu amigo digital para qualquer desafio", width=300)

# --- Mensagem de Boas-Vindas ---
st.write("Bem-vindo ao GATEBOT!")
st.write("⭐ Ei! Tudo bem? Eu sou o GATEBOT, seu parceiro virtual. 😉")
st.write("Tô aqui pra trocar ideia e te ajudar no que for possível!")

# --- Inicialização do Histórico de Conversa (Session State) ---
if 'messages' not in st.session_state:
    st.session_state.messages = []

# --- Exibir Histórico de Conversa ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Entrada de Texto para o Usuário ---
prompt = st.chat_input("Pergunte algo ao GATEBOT...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = get_gemini_response(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

# --- Botão Limpar Conversa ---
st.write("---")
if st.button("Limpar Conversa"):
    st.session_state.messages = []
    st.experimental_rerun()
