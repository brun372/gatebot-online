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
        color: white; /* Cor do texto do botão */
        background-color: #4A4A4A; /* Cor de fundo do botão */
        width: 100%; /* Faz o botão ocupar toda a largura da sidebar */
        margin-bottom: 5px; /* Espaçamento entre os botões */
        border: none; /* Remove a borda padrão do botão */
        text-align: left; /* Alinha o texto do botão à esquerda */
        padding-left: 10px; /* Adiciona um pequeno padding à esquerda */
    }
    .st-emotion-cache-1km1mho button:hover {
        background-color: #6A6A6A; /* Cor de fundo do botão ao passar o mouse */
        color: white; /* Cor do texto ao passar o mouse */
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

# --- Inicialização do Histórico de Conversa (Session State) ---
if 'messages' not in st.session_state:
    st.session_state.messages = []
# Variável para armazenar a pergunta pré-preenchida
if 'pre_filled_prompt' not in st.session_state:
    st.session_state.pre_filled_prompt = ""

# --- Exibir Histórico de Conversa (Área Principal) ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Entrada de Texto para o Usuário (Área Principal) ---
# O 'value' do chat_input agora é preenchido pela session_state.pre_filled_prompt
prompt = st.chat_input("Pergunte algo ao GATEBOT...", value=st.session_state.pre_filled_prompt)

# Se o usuário digitou ou um botão preencheu o prompt, processa
if prompt:
    # Zera o pre_filled_prompt para que não fique preenchido na próxima interação
    st.session_state.pre_filled_prompt = ""

    # Adiciona a pergunta do usuário ao histórico e exibe
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gera a resposta do Gemini
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."): # Mostra um spinner enquanto o Gemini pensa
            response = get_gemini_response(prompt) # Chama a função que interage com a API do Gemini
        st.markdown(response) # Exibe a resposta do Gemini

    # Adiciona a resposta do Gemini ao histórico
    st.session_state.messages.append({"role": "assistant", "content": response})


# --- Conteúdo da Sidebar (Barra Lateral) ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/brun372/gatebot-online/main/B5w10V3.PNG", width=100) # Mini logo ou robo na sidebar
    st.title("GATEBOT Menu")
    st.markdown("---") # Linha divisória

    st.header("Áreas de Conhecimento:")

    # Botões para cada área que pré-preenchem o prompt
    if st.button("📚 Educação"):
        st.session_state.messages = [] # Limpa histórico para nova área
        st.session_state.pre_filled_prompt = "Me conte sobre a Segunda Guerra Mundial."
        st.experimental_rerun() # Recarrega a página para o prompt ser preenchido

    if st.button("💡 Ideias"):
        st.session_state.messages = []
        st.session_state.pre_filled_prompt = "Gere ideias para um projeto de aplicativo de finanças."
        st.experimental_rerun()

    if st.button("👨‍💻 Programação"):
        st.session_state.messages = []
        st.session_state.pre_filled_prompt = "Qual a diferença entre Python e JavaScript?"
        st.experimental_rerun()

    if st.button("🌍 Notícias/Atualidades"):
        st.session_state.messages = []
        st.session_state.pre_filled_prompt = "Quais as notícias mais importantes de hoje?"
        st.experimental_rerun()

    if st.button("🤔 Curiosidades"):
        st.session_state.messages = []
        st.session_state.pre_filled_prompt = "Me diga uma curiosidade interessante sobre o espaço."
        st.experimental_rerun()

    if st.button("❤️‍🩹 Bem-Estar"):
        st.session_state.messages = []
        st.session_state.pre_filled_prompt = "Dê dicas para melhorar a qualidade do sono."
        st.experimental_rerun()

    if st.button("🎲 Jogos/Entretenimento"):
        st.session_state.messages = []
        st.session_state.pre_filled_prompt = "Sugira um jogo online gratuito divertido."
        st.experimental_rerun()

    st.markdown("---") # Outra linha divisória

    # Botão Limpar Conversa (dentro da sidebar para organizar melhor)
    if st.button("Limpar Conversa"): # Pode ter um texto diferente para diferenciar dos outros botões
        st.session_state.messages = []  # Zera o histórico de mensagens
        st.session_state.pre_filled_prompt = "" # Limpa também o prompt pré-preenchido
        st.experimental_rerun()         # Recarrega o aplicativo para refletir a mudança

    st.markdown("---") # Mais uma linha divisória
    st.write("Desenvolvido por Bruno Gabriel") # Sua assinatura
