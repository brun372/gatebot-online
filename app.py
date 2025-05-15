import streamlit as st
import google.generativeai as genai
import os

# --- Configuração do Streamlit ---
st.set_page_config(page_title="GATEBOT: Seu Assistente de IA")

st.title("🤖 GATEBOT")
st.header("Seu Assistente de IA com Google Gemini")

st.write("🌟 Ei! Tudo bem? Eu sou o GATEBOT, seu parceiro virtual. 😉")
st.write("Tô aqui pra trocar ideia e te ajudar no que for possível!")

# --- Configuração da API do Google Gemini (Lendo de VARIÁVEL DE AMBIENTE) ---
# O Streamlit Cloud vai ler esta chave de um "Secret" que você vai configurar lá.
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ ERRO: Sua chave de API `GOOGLE_API_KEY` não foi carregada.")
    st.info("Por favor, configure `GOOGLE_API_KEY` com sua chave real nos 'Secrets' do Streamlit Cloud.")
    st.stop() # Para a execução do aplicativo Streamlit aqui

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- Seleção da Área no Sidebar ---
st.sidebar.header("Escolha sua área:")
area_escolhida = st.sidebar.radio(
    "Em qual dessas áreas você mais precisa de uma força?",
    ("💻 Tecnologia (TI)", "🏥 Saúde e bem-estar", "📚 Estudos e Educação", "💸 Dinheiro e Finanças", "🤔 Outra coisa")
)

st.sidebar.write(f"Sua área selecionada: **{area_escolhida}**")

# Inicializa o histórico do chat se não existir na sessão
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.chat_session = model.start_chat(history=[])

# Exibe o histórico do chat
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Entrada de Perguntas (Chat Input) ---
user_query = st.chat_input("Qual é a sua dúvida ou problema? (Digite 'experty' para encerrar)")

if user_query:
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    if user_query.lower() == 'experty':
        st.session_message = st.chat_message("ai")
        st.session_message.markdown("👋 Foi ótimo conversar com você! Até a próxima! 😊")
        st.session_state.chat_history.append({"role": "ai", "content": "👋 Foi ótimo conversar com você! Até a próxima! 😊"})
        st.stop()

    st.session_message = st.chat_message("ai")
    with st.spinner("🤔 Deixa eu pensar um pouquinho..."):
        try:
            prompt_instruction = (
                f"Você é um assistente virtual chamado GATEBOT. O usuário escolheu a área de '{area_escolhida}'. "
                "Responda à seguinte pergunta de forma útil, amigável, completa e detalhada, "
                "mas sempre organizando o texto com parágrafos claros e, se possível, listas ou tópicos para facilitar a leitura. "
                "Use negritos para destacar informações importantes. "
                "Mantenha um tom acessível, como se estivesse explicando para alguém que está começando. "
                "Se a pergunta for sobre um tópico fora de '{area_escolhida}', mencione isso de forma clara e breve antes de prosseguir com a resposta."
            )

            response = st.session_state.chat_session.send_message(f"{prompt_instruction}\nPergunta: {user_query}")
            ai_response = response.text

            st.session_message.markdown(ai_response)
            st.session_state.chat_history.append({"role": "ai", "content": ai_response})

        except Exception as e:
            error_message = f"Desculpe, algo deu errado ao tentar obter uma resposta (Erro: {e}). Verifique sua conexão com a internet e se sua chave de API está correta e ativa."
            st.session_message.error(error_message)
            st.session_state.chat_history.append({"role": "ai", "content": error_message})