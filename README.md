# 📊 Nexo AI

O **Nexo AI** é um assistente especialista em comunicação corporativa focado em traduzir tópicos soltos e palavras-chave em comunicados claros, coesos e objetivos. Projetado estrategicamente para apoiar líderes de projeto na estruturação de atualizações sobre prazos, gestão de riscos e entregas de dados de forma ágil e padronizada.

## ✨ Funcionalidades

* **Geração Contextualizada:** Transforma tópicos rápidos em textos completos utilizando vocabulário de gestão de projetos ágeis e consultoria.
* **Ajuste de Tom:** * *Formal:* Focado em diretoria, comitês executivos e clientes.
  * *Informal:* Adaptado para o dia a dia da squad, tribos técnicas, Slack ou WhatsApp.
* **Arquitetura de Contingência (Fallback):** O sistema utiliza o modelo **Gemini 2.5 Flash** como motor principal de inferência. Caso haja instabilidade ou limite de cota, a aplicação aciona automaticamente a API da **Cohere (Command-R)** para garantir a disponibilidade do serviço.
* **Compartilhamento Rápido:** Integração direta para envio do texto gerado via WhatsApp e E-mail.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.11
* **Interface Web:** Streamlit
* **Inteligência Artificial:** * Google GenAI SDK (Gemini 2.5 Flash)
  * Cohere API
* **Gerenciamento de Ambiente:** `python-dotenv` e suporte nativo a DevContainers (Docker/Codespaces).

## 🚀 Como Executar Localmente

**1. Clone o repositório**
```bash
git clone [https://github.com/karlarenatadev/nexo-ai.git](https://github.com/karlarenatadev/nexo-ai.git)
cd nexo-ai
```
**2. Crie e ative um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate 
# No Windows: venv\Scripts\activate
# No Linux/Mac: source venv/bin/activate
```
**3. Instale as dependências**
```bash
pip install -r requirements.txt
```
**4. Configure as variáveis de ambiente**
Crie um arquivo `.env` na raiz do projeto e adicione suas chaves de API
```env
GEMINI_API_KEY=sua_chave_gemini_aqui
COHERE_API_KEY=sua_chave_cohere_aqui
```
**5. Execute a aplicação**
```bash
streamlit run app_nexo.py
```
A aplicação estará disponível em `http://localhost:8501`.

## ☁️ Execução via DevContainer / GitHub Codespaces

Este projeto já está configurado com um ficheiro `devcontainer.json`. Se utiliza o VS Code com a extensão Dev Containers ou o GitHub Codespaces, o ambiente será montado automaticamente com o Python 3.11, as extensões necessárias instaladas e as portas mapeadas.

## 📄 Licença

Este projeto está sob a licença MIT. Pode usar, copiar, modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender cópias do Software. O software é fornecido "no estado em que se encontra", sem garantia de qualquer tipo. Em nenhuma circunstância os autores serão responsáveis por qualquer reclamação, danos ou outras responsabilidades.