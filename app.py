import streamlit as st
import google.generativeai as genai
import os

# --- Configuração do Streamlit ---
st.set_page_config(page_title="GATEBOT: Seu Assistente de IA")

st.title("🤖 GATEBOT")
st.header("Seu Assistente de IA com Google Gemini")

# --- Adicionando a Imagem de "Capa" para o Chat ---
# IMPORTANTE: Você precisa substituir "URL_DA_SUA_IMAGEM_AQUI" pelo link REAL da imagem que você quer usar.
# Se você quiser usar a imagem "ChatGPT Image 16 de mai. de 2025, 08_55_28.png",
# você precisará primeiro fazer upload dela para um serviço como Imgur ou GitHub Gist (e obter o link RAW)
# ou para dentro do seu próprio repositório GitHub e pegar o link RAW dela.
# Por exemplo, se fosse uma imagem online:
st.image("https://i.imgur.com/B5w10V3.jpeg", caption="Bem-vindo ao GATEBOT!", width=300)
# Usei um placeholder de imagem do Unsplash. SUBSTITUA PELO SEU LINK!

st.write("🌟 Ei! Tudo bem? Eu sou o GATEBOT, seu parceiro virtual. 😉")
st.write("Tô aqui pra trocar ideia e te ajudar no que for possível!")

# --- Configuração da API do Google Gemini (Lendo de VARIÁVEL DE AMBIENTE) ---
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ ERRO: Sua chave de API `GOOGLE_API_KEY` não foi carregada.")
    st.info("Por favor, configure `GOOGLE_API_KEY` com sua chave real nos 'Secrets' do Streamlit Cloud.")
    st.stop()

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

# Exibe o histórico do chat (incluindo imagens se houver)
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image_url" in message:
            st.image(message["image_url"], caption=message.get("image_caption", ""))

# --- Função para simular pesquisa de imagem (VOCÊ PODE SUBSTITUIR POR UMA API REAL) ---
def get_image_from_query(query_text):
    # Esta é uma SIMULAÇÃO para fins de demonstração.
    # Para uma funcionalidade REAL de busca de imagens, você precisaria integrar uma API
    # como a Google Custom Search API, Bing Image Search API, etc.
    # Exemplo:
    # from Google Search_api import search_image # Se você tivesse uma integração real

    query_text_lower = query_text.lower()
    if "gato" in query_text_lower:
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg", "Um gato fofo"
    elif "cachorro" in query_text_lower:
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Canis_lupus_familiaris_%28Linnaeus%2C_1758%29.jpg/1200px-Canis_lupus_familiaris_%28Linnaeus%2C_1758%29.jpg", "Um cachorro amigável"
    elif "computador" in query_text_lower:
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Computer_desktop_icon.svg/1024px-Computer_desktop_icon.svg.png", "Um computador desktop"
    elif "lua" in query_text_lower:
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/FullMoon2010.jpg/1200px-FullMoon2010.jpg", "A Lua Cheia"
    elif "sol" in query_text_lower:
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Solar_Prominence_from_STEREO_--_September_29%2C_2008.jpg/1200px-Solar_Prominence_from_STEREO_--_September_29%2C_2008.jpg", "O Sol"
    else:
        return None, None

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
                "Se o usuário pedir por uma imagem (ex: 'mostre uma imagem de'), tente encontrar uma imagem relacionada. Use frases como 'Aqui está uma imagem de...'."
            )

            # Primeiro, tenta obter uma resposta de texto do Gemini
            response = st.session_state.chat_session.send_message(f"{prompt_instruction}\nPergunta: {user_query}")
            ai_response = response.text

            st.session_message.markdown(ai_response)
            st.session_state.chat_history.append({"role": "ai", "content": ai_response})

            # --- Lógica para pesquisa de imagens ---
            # Verifica se o usuário pediu uma imagem. Você pode refinar as palavras-chave.
            if any(phrase in user_query.lower() for phrase in ["imagem", "foto", "mostre uma foto", "mostre uma imagem"]):
                # Extrai o que o usuário quer ver na imagem
                image_search_query = user_query.lower()
                image_search_query = image_search_query.replace("mostre uma imagem de", "").replace("imagem de", "").replace("foto de", "").strip()
                
                # Chama a função simulada de pesquisa de imagem
                image_url, image_caption = get_image_from_query(image_search_query)

                if image_url:
                    st.image(image_url, caption=f"Imagem relacionada a: {image_caption}")
                    # Adiciona a imagem ao histórico de forma que possa ser reexibida
                    st.session_state.chat_history.append({"role": "ai", "image_url": image_url, "image_caption": image_caption})
                else:
                    st.session_message.markdown("Desculpe, não consegui encontrar uma imagem para isso no momento na minha base simulada.")
                    st.session_state.chat_history.append({"role": "ai", "content": "Desculpe, não consegui encontrar uma imagem para isso no momento na minha base simulada."})

        except Exception as e:
            error_message = f"Desculpe, algo deu errado ao tentar obter uma resposta (Erro: {e}). Verifique sua conexão com a internet e se sua chave de API está correta e ativa. Detalhe: {e}"
            st.session_message.error(error_message)
            st.session_state.chat_history.append({"role": "ai", "content": error_message})
