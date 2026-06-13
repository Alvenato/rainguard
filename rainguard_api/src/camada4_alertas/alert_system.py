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



import os

# --- DICIONÁRIO DE NÍVEIS QUE O DASHBOARD SOLICITA ---
# Atualizado para conter 'Verde' e outras cores padrão de monitoramento
NIVEIS = {
    "Verde": "🟢 [ESTÁVEL]",
    "Amarelo": "🟡 [ATENÇÃO]",
    "Laranja": "🟠 [ALERTA]",
    "Vermelho": "🔴 [PERIGO]",
    "INFO": "🔵 [INFO]",
    "ALERTA": "⚠️ [ALERTA]",
    "PERIGO": "🚨 [PERIGO]"
}

# --- PROTEÇÃO PARA AMBIENTES EM NUVEM (STREAMLIT CLOUD) ---
try:
    import pywhatkit as kit
    WHATSAPP_DISPONIVEL = True
except (ImportError, ModuleNotFoundError):
    WHATSAPP_DISPONIVEL = False


def emitir_alerta(nivel, mensagem_texto):
    """
    Função principal de alertas do Rainguard. 
    Se estiver local, envia para o WhatsApp. 
    Se estiver na nuvem (Streamlit Cloud), simula o envio nos logs do servidor.
    """
    # Formata o texto final com o nível do alerta
    prefixo = NIVEIS.get(nivel, "📢 [NOTIFICAÇÃO]")
    texto_formatado = f"{prefixo} *RAINGUARD*\n\n{mensagem_texto}"

    # Validação de ambiente Headless / Nuvem
    if not WHATSAPP_DISPONIVEL:
        print("\n⚠️ [Rainguard] Automação de WhatsApp não disponível neste ambiente (Headless/Nuvem).")
        print(f"🖥️ [LOG DO SERVIDOR] Mensagem que seria enviada:\n{texto_formatado}\n")
        return False

    # ID do seu grupo do WhatsApp (extraído do seu link de convite)
    id_do_grupo = "E4sHQ4uQa281FouDjAw1Mw" 
    
    try:
        print(f"\n🔄 [Rainguard] Ambiente local detectado. Abrindo o WhatsApp Web para nível: {nivel}...")
        
        # Executa a automação local abrindo o navegador padrão logado
        kit.sendwhatmsg_to_group_instantly(
            group_id=id_do_grupo,
            message=texto_formatado,
            wait_time=15,
            tab_close=True
        )
        
        print("✅ [Rainguard] Alerta enviado ao grupo do WhatsApp com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ [Rainguard] Falha na automação local do WhatsApp: {e}")
        return False


# --- BLOCO DE TESTE INTERNO ---
if __name__ == "__main__":
    msg_teste = "Modelos analíticos atualizados. Monitoramento operando em estabilidade."
    emitir_alerta("Verde", msg_teste)
