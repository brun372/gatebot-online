import streamlit as st
from gemini_utility import get_gemini_response, configure_api_key

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

# A imagem de capa do GATEBOT, agora hospedada no GitHub e funcionando!
st.image("https://raw.githubusercontent.com/brun372/gatebot-online/main/B5w10V3.PNG", caption="Seu amigo digital para qualquer desafio", width=300)

# --- Mensagem de Boas-Vindas (Área Principal) ---
st.write("Bem-vindo ao GATEBOT!")
st.write("⭐ Ei! Tudo bem? Eu sou o GATEBOT, seu parceiro virtual. 😉")
st.write("Tô aqui pra trocar ideia e te ajudar no que for possível!")

# --- Inicialização do Histórico de Conversa e Valor do Chat Input (Session State) ---
if 'messages' not in st.session_state:
    st.session_state.messages = []
# Nova variável para controlar o valor do chat_input
if 'chat_input_value' not in st.session_state:
    st.session_state.chat_input_value = ""

# --- Exibir Histórico de Conversa (Área Principal) ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Função para Lidar com o Envio da Pergunta ---
def handle_submit():
    # Pega o prompt do chat_input
    prompt = st.session_state.chat_input_key
    if prompt: # Apenas se houver algo digitado/preenchido
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
        # Limpa o chat_input após o envio
        st.session_state.chat_input_value = "" # Define o valor para vazio para limpar o input


# --- Entrada de Texto para o Usuário (Área Principal) ---
# Usamos 'key' e 'on_change' para interagir com o st.chat_input de forma mais robusta.
# O 'value' é definido pela st.session_state.chat_input_value
st.chat_input(
    "Pergunte algo ao GATEBOT...",
    key="chat_input_key", # A chave para acessar o valor do input
    on_change=handle_submit, # A função que é chamada quando o input é alterado (e enter pressionado)
    value=st.session_state.chat_input_value # O valor inicial/pre-preenchido do input
)


# --- Conteúdo da Sidebar (Barra Lateral) ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/brun372/gatebot-online/main/B5w10V3.PNG", width=100) # Mini logo ou robo na sidebar
    st.title("GATEBOT Menu")
    st.markdown("---")

    st.header("Áreas de Conhecimento:")

    # Funções para pré-preencher o prompt
    def set_prompt(text):
        st.session_state.chat_input_value = text
        # Não precisamos de st.experimental_rerun() aqui se o input já estiver no estado.
        # A atualização do valor no session_state já força o redraw.

    if st.button("📚 Educação"):
        st.session_state.messages = [] # Limpa histórico
        set_prompt("Me conte sobre a Segunda Guerra Mundial.")

    if st.button("💡 Ideias"):
        st.session_state.messages = []
        set_prompt("Gere ideias para um projeto de aplicativo de finanças.")

    if st.button("👨‍💻 Programação"):
        st.session_state.messages = []
        set_prompt("Qual a diferença entre Python e JavaScript?")

    if st.button("🌍 Notícias/Atualidades"):
        st.session_state.messages = []
        set_prompt("Quais as notícias mais importantes de hoje?")

    if st.button("🤔 Curiosidades"):
        st.session_state.messages = []
        set_prompt("Me diga uma curiosidade interessante sobre o espaço.")

    if st.button("❤️‍🩹 Bem-Estar"):
        st.session_state.messages = []
        set_prompt("Dê dicas para melhorar a qualidade do sono.")

    if st.button("🎲 Jogos/Entretenimento"):
        st.session_state.messages = []
        set_prompt("Sugira um jogo online gratuito divertido.")

    st.markdown("---")

    # Botão Limpar Conversa
    if st.button("Limpar Conversa"):
        st.session_state.messages = []
        st.session_state.chat_input_value = "" # Limpa o valor do input
        st.experimental_rerun() # Para garantir que a limpeza seja visível imediatamente

    st.markdown("---")
    st.write("Desenvolvido por Bruno Gabriel")
