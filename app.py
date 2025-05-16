import streamlit as st
from gemini_utility import get_gemini_response, configure_api_key

# Configura a API Key do Gemini usando st.secrets (boa prática de segurança)
configure_api_key()

# --- Configurações da Página ---
st.set_page_config(page_title="GATEBOT - Seu Assistente de IA", page_icon="🤖")

# --- CSS Personalizado para a Sidebar ---
# Este bloco de CSS foi adicionado no início para estilizar a sidebar.
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
# Isso garante que o histórico da conversa seja mantido entre as interações.
if 'messages' not in st.session_state:
    st.session_state.messages = []

# --- Exibir Histórico de Conversa ---
# Isso mostra todas as mensagens anteriores na tela.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Entrada de Texto para o Usuário ---
# Aqui o usuário digita sua pergunta.
prompt = st.chat_input("Pergunte algo ao GATEBOT...")

if prompt:
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

# --- Botão Limpar Conversa ---
# Este botão foi adicionado no final da área principal.
# Ele limpa o histórico de mensagens e recarrega a página.
st.write("---") # Adiciona uma linha horizontal para separar o botão
if st.button("Limpar Conversa"):
    st.session_state.messages = []  # Zera o histórico de mensagens
    st.experimental_rerun()         # Recarrega o aplicativo para refletir a mudança
