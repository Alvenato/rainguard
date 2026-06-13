# from loguru import logger
# import os

# try:
#     from dotenv import load_dotenv
#     load_dotenv()
# except ImportError:
#     logger.warning("Biblioteca 'python-dotenv' não encontrada. Variáveis de ambiente serão lidas do sistema.")

# try:
#     from twilio.rest import Client
#     _TWILIO_AVAILABLE = True
# except ImportError:
#     Client = None
#     _TWILIO_AVAILABLE = False
#     logger.warning("Biblioteca 'twilio' não encontrada. Alertas WhatsApp estarão desativados.")

# # Configurações da API
# account_sid = os.getenv("TWILIO_ACCOUNT_SID", "AC2997f388cd052e65d40263836a6b6b57")
# auth_token = os.getenv("TWILIO_AUTH_TOKEN", "0a311ebe0d6723eeb1bd2e68076fe5f2")

# client = None
# if _TWILIO_AVAILABLE and account_sid and auth_token:
#     client = Client(account_sid, auth_token)
# elif _TWILIO_AVAILABLE:
#     logger.warning("Twilio encontrado, mas as credenciais TWILIO_ACCOUNT_SID ou TWILIO_AUTH_TOKEN não estão configuradas.")

# TWILIO_FROM = "whatsapp:+14155238886"

# DESTINATARIOS = [
#     "whatsapp:+556181830780",
#     "whatsapp:+556199445562",
#     "whatsapp:+556199655321",
#     "whatsapp:+556182417170",
#     "whatsapp:+556181515868"
# ]

# NIVEIS = {
#     "Verde":    {"cor": "🟢", "acao": "Monitoramento normal"},
#     "Amarelo":  {"cor": "🟡", "acao": "Atenção — acompanhar previsão"},
#     "Laranja":  {"cor": "🟠", "acao": "Alerta — notificar Defesa Civil"},
#     "Vermelho": {"cor": "🔴", "acao": "CRÍTICO — evacuar área de risco"},
# }

# def emitir_alerta(regiao_id: str, nivel: str, dados: dict, recipients: list | None = None) -> str:
#     info = NIVEIS.get(nivel, NIVEIS["Verde"])

#     mensagem = (
#         f"{info['cor']} RAINGUARD — Região {regiao_id}\n"
#         f"Nível: {nivel} | Ação: {info['acao']}\n"
#         f"Chuva: {dados.get('precipitacao', 0):.1f}mm | "
#         f"Rio: {dados.get('nivel_rio', 0):.1f}m | "
#         f"Umidade: {dados.get('umidade', 0):.0f}%"
#     )

#     logger.info(mensagem)

#     targets = recipients if recipients else DESTINATARIOS

#     if client is None:
#         logger.warning("Twilio não está disponível ou não foi configurado. O alerta será registrado somente no log.")
#         return mensagem

#     for numero in targets:
#         try:
#             response = client.messages.create(
#                 from_=TWILIO_FROM,
#                 body=mensagem,
#                 to=numero
#             )

#             logger.success(
#                 f"WhatsApp enviado para {numero}. SID: {response.sid}"
#             )

#         except Exception as exc:
#             logger.error(
#                 f"Falha ao enviar para {numero}: {exc}"
#             )

#     return mensagem







import pywhatkit as kit
import time

def enviar_alerta_grupo_whatsapp(mensagem_texto):
    """
    Dispara alertas do Rainguard direto para o grupo de WhatsApp
    utilizando automação via navegador.
    """
    # Seu ID de grupo extraído do link de convite
    id_do_grupo = "E4sHQ4uQa281FouDjAw1Mw" 
    
    try:
        print("\n🔄 [Rainguard] Abrindo o WhatsApp Web e preparando o envio...")
        
        # Envia a mensagem instantaneamente. 
        # wait_time=15 dá tempo do navegador abrir e carregar o chat do grupo.
        # tab_close=True fecha a aba do navegador automaticamente após o envio.
        kit.sendwhatmsg_to_group_instantly(
            group_id=id_do_grupo,
            message=mensagem_texto,
            wait_time=15,
            tab_close=True
        )
        
        print("✅ [Rainguard] Alerta enviado ao grupo com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ [Rainguard] Falha ao tentar enviar mensagem: {e}")
        return False

# --- TESTE ISOLADO DO SCRIPT ---
if __name__ == "__main__":
    texto_teste = (
        "🌧️ *ALERTA RAINGUARD*\n\n"
        "Atenção: Sistema de monitoramento online. Modelos analíticos "
        "reconfigurados com sucesso para alertas em grupo!"
    )
    enviar_alerta_grupo_whatsapp(texto_teste)
