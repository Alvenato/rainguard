from fastapi import FastAPI, Form, Response
from loguru import logger
import requests
import os

app = FastAPI(title="RainGuard Webhook Forwarder")

# Configurações do seu WhatsApp Automatizado (Evolution API, Wppconnect ou similar)
# Deixei apontado para o padrão local, ajuste quando tiver sua instância pronta
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL", "http://localhost:8080/message/sendText/rainguard")
WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY", "SUA_API_KEY_AQUI")
ID_DO_GRUPO_WHATSAPP = os.getenv("ID_GRUPO_WHATSAPP", "120363043210987654@g.us")

@app.post("/twilio-webhook")
async def receber_e_redirecionar(
    From: str = Form(...),
    Body: str = Form(...)
):
    """
    Recebe as mensagens automáticas enviadas pelo Twilio e repassa
    diretamente para o grupo do WhatsApp da equipe.
    """
    logger.info(f"📩 Mensagem capturada do Twilio (Origem: {From}): {Body}")

    # Formatação do alerta que vai cair no grupo do WhatsApp
    mensagem_para_grupo = (
        f"🔄 *[RainGuard - Redirecionador]*\n\n"
        f"📱 *Origem:* {From}\n"
        f"💬 *Mensagem:* {Body}"
    )

    # Payload para injetar a mensagem na API do WhatsApp
    headers = {
        "apikey": WHATSAPP_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "number": ID_DO_GRUPO_WHATSAPP,
        "text": mensagem_para_grupo
    }

    try:
        # Envia a requisição POST para a API do WhatsApp Web
        response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers, timeout=10)
        
        if response.status_code in [200, 201]:
            logger.success("✅ Alerta redirecionado para o grupo com sucesso!")
        else:
            logger.error(f"❌ Erro na API do WhatsApp ({response.status_code}): {response.text}")
            
    except Exception as exc:
        logger.error(f"💥 Falha crítica de conexão com a API do WhatsApp: {exc}")

    # Retorna o XML vazio (TwiML) exigido pelo Twilio para confirmar o recebimento
    return Response(content="<Response></Response>", media_type="application/xml")
