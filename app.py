import streamlit as st
from gemini_utility import get_gemini_response, configure_api_key

# Configura a API Key do Gemini usando st.secrets
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
    /* Estilo para os botões da sidebar (cor do texto e do fundo ao passar o mouse) */
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

# --- Função para Processar uma Pergunta (usada tanto pelo chat_input quanto pelos botões) ---
def process_question(question):
    # Adiciona a pergunta do usuário ao histórico e exibe
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Gera a resposta do Gemini
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = get_gemini_response(question)
        st.markdown(response)

    # Adiciona a resposta do Gemini ao histórico
    st.session_state.messages.append({"role": "assistant", "content": response})

# --- Entrada de Texto para o Usuário (Área Principal) ---
# O chat_input continua funcionando normalmente para perguntas digitadas.
# Não adicionamos 'value' ou 'on_change' para evitar o TypeError.
prompt = st.chat_input("Pergunte algo ao GATEBOT...")

if prompt:
    process_question(prompt)


# --- Conteúdo da Sidebar (Barra Lateral) ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/brun372/gatebot-online/main/B5w10V3.PNG", width=100) # Mini logo ou robo na sidebar
    st.title("GATEBOT Menu")
    st.markdown("---")

    st.header("Áreas de Conhecimento:")

    # Botões para cada área que DISPARAM A PERGUNTA IMEDIATAMENTE
    # Ao clicar, limpa o histórico e envia uma pergunta pré-definida.
    if st.button("📚 Educação"):
        st.session_state.messages = [] # Limpa histórico para nova conversa sobre o tema
        process_question("Me conte sobre a Segunda Guerra Mundial.")
        st.experimental_rerun() # Recarrega para mostrar o novo histórico e a resposta

    if st.button("💡 Ideias"):
        st.session_state.messages = []
        process_question("Gere ideias para um projeto de aplicativo de finanças.")
        st.experimental_rerun()

    if st.button("👨‍💻 Programação"):
        st.session_state.messages = []
        process_question("Qual a diferença entre Python e JavaScript?")
        st.experimental_rerun()

    if st.button("🌍 Notícias/Atualidades"):
        st.session_state.messages = []
        process_question("Quais as notícias mais importantes de hoje?")
        st.experimental_rerun()

    if st.button("🤔 Curiosidades"):
        st.session_state.messages = []
        process_question("Me diga uma curiosidade interessante sobre o espaço.")
        st.experimental_rerun()

    if st.button("❤️‍🩹 Bem-Estar"):
        st.session_state.messages = []
        process_question("Dê dicas para melhorar a qualidade do sono.")
        st.experimental_rerun()

    if st.button("🎲 Jogos/Entretenimento"):
        st.session_state.messages = []
        process_question("Sugira um jogo online gratuito divertido.")
        st.experimental_rerun()

    st.markdown("---")

    # Botão Limpar Conversa (dentro da sidebar)
    if st.button("Limpar Conversa"):
        st.session_state.messages = []
        st.experimental_rerun() # Recarrega o aplicativo para refletir a mudança

    st.markdown("---")
    st.write("Desenvolvido por Bruno Gabriel")
