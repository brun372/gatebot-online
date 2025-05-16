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
    .st-emotion-cache-nahz7x { /* Esta é a classe CSS comum para a sidebar */
        background-color: #262730;
    }
    /* Estilo para o texto do sidebar. Você pode mudar a cor e o tamanho da fonte. */
    .st-emotion-cache-1pxazr6 { /* Esta é a classe CSS comum para texto na sidebar */
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
# Variável para armazenar a pergunta pré-preenchida. Usaremos uma chave para o input.
if 'pre_filled_prompt_key' not in st.session_state:
    st.session_state.pre_filled_prompt_key = 0 # Usado para resetar o valor do input

# --- Exibir Histórico de Conversa (Área Principal) ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Entrada de Texto para o Usuário (Área Principal) ---
# O truque para pré-preencher o chat_input é usar uma 'key' que muda.
# Quando a key muda, o Streamlit considera que é um novo widget e recarrega com o valor padrão.
# A pergunta pré-preenchida é armazenada temporariamente.
temp_prompt_value = ""
if "new_pre_filled_prompt" in st.session_state:
    temp_prompt_value = st.session_state.new_pre_filled_prompt
    # st.session_state.new_pre_filled_prompt é consumido depois de ser usado
    del st.session_state.new_pre_filled_prompt


prompt = st.chat_input("Pergunte algo ao GATEBOT...", key=f"chat_input_{st.session_state.pre_filled_prompt_key}", value=temp_prompt_value)


# Se o usuário digitou ou um botão preencheu o prompt, processa
if prompt:
    # Incrementa a key para que o input possa ser resetado na próxima vez que um botão for clicado
    st.session_state.pre_filled_prompt_key += 1

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
    # A lógica aqui é colocar o valor no new_pre_filled_prompt e forçar um rerun.
    if st.button("📚 Educação"):
        st.session_state.messages = [] # Limpa histórico para nova área
        st.session_state.new_pre_filled_prompt = "Me conte sobre a Segunda Guerra Mundial."
        st.session_state.pre_filled_prompt_key += 1 # Garante que o input será resetado
        st.experimental_rerun() # Recarrega a página para o prompt ser preenchido

    if st.button("💡 Ideias"):
        st.session_state.messages = []
        st.session_state.new_pre_filled_prompt = "Gere ideias para um projeto de aplicativo de finanças."
        st.session_state.pre_filled_prompt_key += 1
        st.experimental_rerun()

    if st.button("👨‍💻 Programação"):
        st.session_state.messages = []
        st.session_state.new_pre_filled_prompt = "Qual a diferença entre Python e JavaScript?"
        st.session_state.pre_filled_prompt_key += 1
        st.experimental_rerun()

    if st.button("🌍 Notícias/Atualidades"):
        st.session_state.messages = []
        st.session_state.new_pre_filled_prompt = "Quais as notícias mais importantes de hoje?"
        st.session_state.pre_filled_prompt_key += 1
        st.experimental_rerun()

    if st.button("🤔 Curiosidades"):
        st.session_state.messages = []
        st.session_state.new_pre_filled_prompt = "Me diga uma curiosidade interessante sobre o espaço."
        st.session_state.pre_filled_prompt_key += 1
        st.experimental_rerun()

    if st.button("❤️‍🩹 Bem-Estar"):
        st.session_state.messages = []
        st.session_state.new_pre_filled_prompt = "Dê dicas para melhorar a qualidade do sono."
        st.session_state.pre_filled_prompt_key += 1
        st.experimental_rerun()

    if st.button("🎲 Jogos/Entretenimento"):
        st.session_state.messages = []
        st.session_state.new_pre_filled_prompt = "Sugira um jogo online gratuito divertido."
        st.session_state.pre_filled_prompt_key += 1
        st.experimental_rerun()

    st.markdown("---") # Outra linha divisória

    # Botão Limpar Conversa (dentro da sidebar para organizar melhor)
    if st.button("Limpar Conversa"):
        st.session_state.messages = []
        # Para limpar o chat_input quando o botão limpar é clicado
        if "new_pre_filled_prompt" in st.session_state:
            del st.session_state.new_pre_filled_prompt
        st.session_state.pre_filled_prompt_key += 1 # Garante que o input será resetado
        st.experimental_rerun()

    st.markdown("---") # Mais uma linha divisória
    st.write("Desenvolvido por Bruno Gabriel")
