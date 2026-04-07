import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Carrega as senhas ocultas do arquivo .env
load_dotenv()

# Puxa a chave de forma segura
CHAVE_API = os.getenv("GEMINI_API_KEY")

# Inicia o cliente do Gemini
cliente = genai.Client(api_key=CHAVE_API)

instrucoes_sistema = """
Você é o Nexo AI, um assistente especialista em comunicação corporativa exclusivo para os CLPs (Consultores Líderes de Projeto) da A3Data.
Sua função é transformar palavras-chave em textos coesos, claros e objetivos sobre projetos de dados, gestão de riscos, prazos e entregas.

REGRAS:
1. Conecte as palavras-chave de forma lógica, criando um fluxo de informação claro sobre o status do projeto.
2. Utilize vocabulário de gestão de projetos ágeis e consultoria de dados (ex: mitigação, stakeholders, sprint, pipeline, on track, delay, deploy).
3. Se o tom for "Formal", escreva focado em clientes, diretoria ou comitês executivos. Seja polido, focado em impacto e soluções.
4. Se o tom for "Informal", escreva para a squad técnica, tribo ou para o WhatsApp do cliente de forma mais leve, ágil e parceira, mas sem perder o profissionalismo.
5. Quando o assunto for "Risco" ou "Atraso", seja transparente, mas sempre adicione um tom de que a equipe já está buscando a solução (proatividade).
6. Entregue APENAS o texto gerado, sem saudações iniciais ou explicações do que você fez.
"""

# Configuração do modelo e das instruções
configuracao_modelo = types.GenerateContentConfig(
    system_instruction=instrucoes_sistema,
)

# 2. Interface de Usuário com Streamlit
st.set_page_config(page_title="Nexo AI | A3Data", page_icon="📊")

st.title("📊 Nexo AI: Alinhamento de Projetos")
st.markdown("**Exclusivo para CLPs A3Data** - Transforme tópicos em comunicados claros sobre prazos, riscos e status de projetos.")

# Campos de entrada
st.write("---")
palavras_chave = st.text_area(
    "Insira as palavras-chave ou tópicos soltos:", 
    placeholder="Ex: risco mapeado na ingestão de dados, sprint 3 atrasada 2 dias, prazo final mantido, plano de ação alinhado com engenharia."
)

col1, col2 = st.columns(2)

with col1:
    tom = st.radio(
        "Selecione o público/tom da mensagem:", 
        ["Formal (Cliente / Comitê / E-mail Oficial)", "Informal (Squad / Slack / WhatsApp)"]
    )

with col2:
    st.write("") # Espaçamento
    st.write("")
    botao_gerar = st.button("Gerar Comunicado", type="primary", use_container_width=True)

# 3. Lógica de Geração
if botao_gerar:
    if not palavras_chave:
        st.warning("Por favor, insira os tópicos ou palavras-chave do projeto primeiro.")
    else:
        with st.spinner("O Nexo AI está estruturando o alinhamento..."):
            try:
                # Montando o prompt
                prompt_usuario = f"Escreva um comunicado no tom '{tom}' utilizando as seguintes informações/palavras-chave: {palavras_chave}"
                
                # Chamando a nova API
                resposta = cliente.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt_usuario,
                    config=configuracao_modelo
                )
                
                # Exibindo o resultado
                st.success("Comunicado gerado com sucesso!")
                st.text_area("Copie o texto abaixo:", value=resposta.text, height=350)
                
            except Exception as e:
                st.error(f"Ocorreu um erro ao conectar com a IA: {e}")