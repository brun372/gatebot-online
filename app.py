import streamlit as st
from gemini_utility import get_gemini_response, configure_api_key

# Configura a API Key do Gemini usando st.secrets (boa prática de segurança)
configure_api_key()

# --- Configurações da Página ---
st.set_page_config(page_title="GATEBOT - Seu Assistente de IA", page_icon="🤖")

# --- CSS Personalizado para a Sidebar ---
st.markdown("""
<style>
    /* Estilo para a cor de fundo da sidebar. */
    .st-emotion-cache-nahz7x {
        background-color: #262730;
    }
    /* Estilo para o texto do sidebar. */
    .st-emotion-cache-1pxazr6 {
        color: white;
    }
    /* Estilo para botões na sidebar (cor do texto e do fundo ao passar o mouse) */
    .st-emotion-cache-1km1mho button {
        color: white;
        background-color: #4A4A4A;
        width: 100%;
        margin-bottom: 5px;
        border: none;
        text-align: left;
        padding-left: 10px;
    }
    .st-emotion-cache-1km1mho button:hover {
        background-color: #6A6A6A;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# --- Título e Imagem de Capa (Área Principal) ---
st.title("GATEBOT")
st.header("Seu Assistente de IA com Google Gemini")

# A imagem de capa do GATEBOT, hospedada no GitHub.
st.image("https://raw.githubusercontent.com/brun372/gatebot-online/main/B5w10V3.PNG", caption="Seu amigo digital para qualquer desafio", width=300)

# --- Mensagem de Boas-Vindas (Área Principal) ---
st.write("Bem-vindo ao GATEBOT!")
st.write("⭐ Ei! Tudo bem? Eu sou o GATEBOT, seu parceiro virtual. 😉")
st.write("Tô aqui pra trocar ideia e te ajudar no que for possível!")

# --- Inicialização do Histórico de Conversa (Session State) ---
if 'messages' not in st.session_state:
    st.session_state.messages = []

# --- Exibir Histórico de Conversa (Área Principal) ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Entrada de Texto para o Usuário (Área Principal) ---
prompt = st.chat_input("Pergunte algo ao GATEBOT...")

if prompt:
    # Adiciona a pergunta do usuário ao histórico e exibe
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera a resposta do Gemini
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = get_gemini_response(prompt)
        st.markdown(response)

    # Adiciona a resposta do Gemini ao histórico
    st.session_state.messages.append({"role": "assistant", "content": response})


# --- Conteúdo da Sidebar (Barra Lateral) ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/brun372/gatebot-online/main/B5w10V3.PNG", width=100) # Mini logo ou robo na sidebar
    st.title("GATEBOT Menu")
    st.markdown("---")

    st.header("Áreas de Conhecimento:")
    # Áreas de conhecimento como texto, sem funcionalidade de clique para perguntar
    st.write("📚 **Educação:** Perguntas sobre história, ciência, literatura.")
    st.write("💡 **Ideias:** Brainstorming, criatividade, soluções de problemas.")
    st.write("👨‍💻 **Programação:** Dúvidas sobre código, lógica, linguagens.")
    st.write("🌍 **Notícias/Atualidades:** Resumo de eventos, informações gerais.")
    st.write("🤔 **Curiosidades:** Fatos aleatórios, explicações simples.")
    st.write("❤️‍🩹 **Bem-Estar:** Dicas de saúde, hobbies, autoajuda.")
    st.write("🎲 **Jogos/Entretenimento:** Sugestões, regras, informações.")

    st.markdown("---")

    # Botão Limpar Conversa (continua funcionando)
    if st.button("Limpar Conversa"):
        st.session_state.messages = []
        st.experimental_rerun()

    st.markdown("---")
    st.write("Desenvolvido por Bruno Gabriel")
