import streamlit as st
import os
import urllib.parse
from st_copy_to_clipboard import st_copy_to_clipboard
from dotenv import load_dotenv
from google import genai
from google.genai import types
import cohere # IA DE CONTINGÊNCIA

# 1. Carregamento de Credenciais
load_dotenv()

# Chave do Gemini
CHAVE_GEMINI = os.getenv("GEMINI_API_KEY")
if not CHAVE_GEMINI:
    try:
        CHAVE_GEMINI = st.secrets["GEMINI_API_KEY"]
    except:
        st.error("⚠️ Chave do Gemini não encontrada.")
        st.stop()

# Chave da Cohere (Fallback)
CHAVE_COHERE = os.getenv("COHERE_API_KEY")
if not CHAVE_COHERE:
    try:
        CHAVE_COHERE = st.secrets["COHERE_API_KEY"]
    except:
        st.error("⚠️ Chave da Cohere não encontrada.")
        st.stop()

# Inicia os clientes
cliente_gemini = genai.Client(api_key=CHAVE_GEMINI)
cliente_cohere = cohere.Client(api_key=CHAVE_COHERE)

instrucoes_sistema = """
Você é o Nexo AI, um assistente especialista em comunicação corporativa exclusivo para os CLPs (Consultores Líderes de Projeto) da A3Data.
Sua função é transformar palavras-chave em textos coesos, claros e objetivos sobre projetos de dados, gestão de riscos, prazos e entregas.

REGRAS:
1. Conecte as palavras-chave de forma lógica, criando um fluxo de informação claro sobre o status do projeto.
2. Utilize vocabulário de gestão de projetos ágeis e consultoria de dados (ex: mitigação, stakeholders, sprint, pipeline, on track, delay, deploy).
3. Se o tom for "Formal", escreva focado em clientes, diretoria ou comitês executivos. Seja polido, focado em impacto e soluções. MANTENHA O TEXTO CURTO, CONCISO E DIRETO AO PONTO.
4. Se o tom for "Informal", escreva para a squad técnica, tribo ou para o WhatsApp do cliente de forma mais leve, ágil e parceira.
5. Quando o assunto for "Risco" ou "Atraso", seja transparente, mas sempre adicione um tom de que a equipe já está buscando a solução.
6. Entregue APENAS o texto gerado, sem saudações iniciais ou explicações do que você fez.
7. REGRA CRÍTICA DE FORMATAÇÃO: NUNCA utilize asteriscos (*), hashtags (#) ou qualquer formatação Markdown. Entregue o texto em formato plano (plain text) puro.
8. FILTRO DE CNV: Se o usuário inserir desabafos, reclamações pessoais ou linguagem agressiva (ex: "fulano é preguiçoso"), transforme o texto usando Comunicação Não-Violenta. Foque no processo, nos gargalos e na solução, nunca atacando o indivíduo.
9. ANTI-ALUCINAÇÃO: Nunca invente prazos, métricas ou nomes que não foram fornecidos nas palavras-chave. Se faltar alguma informação essencial para o contexto, utilize marcadores como [INSERIR DATA] ou [INSERIR NOME].
10. CALL TO ACTION (CTA): Sempre finalize o comunicado sugerindo um próximo passo claro (ex: pedir uma aprovação, sugerir uma call de alinhamento ou pedir confirmação de leitura).
"""
configuracao_gemini = types.GenerateContentConfig(
    system_instruction=instrucoes_sistema,
)

# 2. Interface de Usuário
st.set_page_config(page_title="Nexo AI | A3Data", page_icon="📊")

st.title("📊 Nexo AI: Alinhamento de Projetos")
st.markdown("**Exclusivo para CLPs A3Data** - Transforme tópicos em comunicados claros sobre prazos, riscos e status de projetos.")

st.write("---")
palavras_chave = st.text_area(
    "Insira as palavras-chave ou tópicos soltos:", 
    placeholder="Ex: risco mapeado na ingestão de dados, sprint 3 atrasada 2 dias, prazo final mantido, plano de ação alinhado."
)

col1, col2 = st.columns(2)

with col1:
    tom = st.radio(
        "Selecione o público/tom da mensagem:", 
        ["Formal (Cliente / Comitê / E-mail Oficial)", "Informal (Squad / Slack / WhatsApp)"]
    )

with col2:
    st.write("") 
    st.write("")
    botao_gerar = st.button("Gerar Comunicado", type="primary", use_container_width=True)

# 3. Lógica de Geração com Fallback
if botao_gerar:
    if not palavras_chave:
        st.warning("Por favor, insira os tópicos ou palavras-chave do projeto primeiro.")
    else:
        with st.spinner("O Nexo AI está estruturando o alinhamento..."):
            texto_gerado = None
            prompt_usuario = f"Escreva um comunicado no tom '{tom}' utilizando estas informações: {palavras_chave}"
            
            try:
                # --- PLANO A: GOOGLE GEMINI (Mantido o 2.5 conforme você pediu) ---
                resposta = cliente_gemini.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt_usuario,
                    config=configuracao_gemini
                )
                texto_gerado = resposta.text
                st.success("Gerado via Google Gemini")

            except Exception as e_gemini:
                # --- PLANO B: COHERE (Novo Fallback) ---
                st.warning("Gemini 2.5 sem cota ou instável. Acionando contingência (Cohere)...")
                try:
                    resposta_cohere = cliente_cohere.chat(
                        model="command-r", # Modelo excelente para textos corporativos
                        preamble=instrucoes_sistema, # A Cohere chama as instruções de sistema de 'preamble'
                        message=prompt_usuario
                    )
                    texto_gerado = resposta_cohere.text
                    st.success("Gerado via rede de contingência Cohere")
                
                except Exception as e_cohere:
                    print(f"Erro Gemini: {e_gemini}")
                    print(f"Erro Cohere: {e_cohere}")
                    st.error("Erro Crítico: Ambos os serviços falharam. Verifique o terminal para detalhes.")
                    st.stop()
            
            # --- RESULTADO E COMPARTILHAMENTO ---
            if texto_gerado:
                st.subheader("📝 Seu Comunicado")

                num_linhas = texto_gerado.count('\n') + 5

                altura_dinamica = max(200, num_linhas * 25)

                texto_final = st.text_area(
                    "Revise e edite se necessário:", 
                    value=texto_gerado, 
                    height=altura_dinamica)

                st_copy_to_clipboard(texto_final, before_copy_label="📋 Copiar comunicado")
                    
                st.markdown("### 🚀 Enviar Para:")

                texto_codificado = urllib.parse.quote(texto_final) 
                
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    link_wpp = f"https://api.whatsapp.com/send?text={texto_codificado}"
                    st.link_button("📱 WhatsApp", link_wpp, use_container_width=True)
                    
                with col_btn2:
                    link_email = f"mailto:?subject=Alinhamento%20Projeto%20A3Data&body={texto_codificado}"
                    st.link_button("✉️ E-mail", link_email, use_container_width=True)