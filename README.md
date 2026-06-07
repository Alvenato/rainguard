# RainGuard

Aplicação Streamlit para previsão e alerta de enchentes.

Como executar localmente:

1. Criar e ativar um virtualenv (recomendado):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1  # PowerShell
# ou
venv\Scripts\activate.bat  # CMD
```

2. Instalar dependências:

```powershell
pip install -r requirements.txt
```

3. Rodar o app Streamlit:

```powershell
streamlit run rainguard_api/dashboard.py
```

Rodando no Streamlit Community Cloud:

- Faça o push deste repositório para o GitHub (branch `main`).
- No Streamlit Cloud, crie um novo app apontando para este repositório e configure o arquivo a executar como `rainguard_api/dashboard.py`.
- O Streamlit Cloud instalará o `requirements.txt` na raiz automaticamente.

Observações:
- Se desejar envio de alertas via WhatsApp/WhatsApp Business, configure as variáveis `TWILIO_ACCOUNT_SID` e `TWILIO_AUTH_TOKEN` no painel de Secrets do Streamlit (ou em `.env` localmente) e instale `python-dotenv`.
- O projeto contém um `.gitignore` que exclui `venv` e arquivos temporários; certifique-se de não commitar ambientes virtuais.
