from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request as flask_request
import threading
import requests
import os
import time

# ─── CONFIG ──────────────────────────────────────────────────────────────────
TOKEN = os.getenv("TOKEN")
INFINITE_TAG = os.getenv("INFINITE_TAG")       # sua InfiniteTag sem o $
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")     # 590895242
BASE_URL = os.getenv("BASE_URL")               # https://mavra-production.up.railway.app

VIP_LINK = "https://t.me/+KN3vIstR8B1kZjEx"

# LINKS
MEXC_LINK = "https://promote.mexc.com/b/wallstreetgirls"
BINGX_LINK = "https://bingx.com/partner/wallstreetgirls"
SUPORTE_LINK = "https://t.me/suportewsg"

YOUTUBE_LINK = "https://youtube.com/@wallstreet_girls"
TIKTOK_LINK = "https://tiktok.com/@wallstreet.girls"
INSTAGRAM_LINK = "https://instagram.com/wallstreet_girls"

uids_validos = ["123456", "789101", "555999"]
aguardando_uid = set()

# Sessões para fluxo de cobrança
sessions = {}

# ─── HELPERS INFINITEPAY ─────────────────────────────────────────────────────
def gerar_link_pagamento(descricao, valor_centavos, cliente_nome=None, recorrente=False, periodicidade="monthly"):
    payload = {
        "handle": INFINITE_TAG,
        "redirect_url": f"{BASE_URL}/obrigado",
        "webhook_url": f"{BASE_URL}/webhook/infinitepay",
        "order_nsu": f"order_{int(time.time())}",
        "items": [
            {
                "quantity": 1,
                "price": valor_centavos,
                "description": descricao
            }
        ]
    }

    if cliente_nome:
        payload["customer"] = {"name": cliente_nome}

    if recorrente:
        payload["recurrence"] = {"frequency": periodicidade}

    resp = requests.post(
        "https://api.infinitepay.io/invoices/public/checkout/links",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("url") or data.get("checkout_url") or data.get("link")

def formatar_valor(centavos):
    return f"R$ {centavos/100:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ─── START ────────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔐 Intel Zone (VIP)", callback_data="vip")],
        [InlineKeyboardButton("⚡ Sinais (parceria)", callback_data="sinais")],
        [InlineKeyboardButton("🎓 Mentoria", callback_data="mentoria")],
        [InlineKeyboardButton("📊 Conteúdo gratuito", callback_data="conteudo")],
        [InlineKeyboardButton("💳 Pagamento / Assinatura", callback_data="pagamento")],
        [InlineKeyboardButton("💬 Suporte", url=SUPORTE_LINK)]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "💎 *Wall Street Girls*\n\n"
        "Um ecossistema para quem quer operar com estratégia e consistência.\n\n"
        "Aqui você não depende de sorte.\n"
        "Você aprende a ler o mercado.\n\n"
        "👇 Escolha como quer começar:",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# ─── CLIQUES ──────────────────────────────────────────────────────────────────
async def escolha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.from_user.id

    # VIP
    if query.data == "vip":
        aguardando_uid.add(chat_id)

        keyboard = [
            [InlineKeyboardButton("📲 Criar conta MEXC", url=MEXC_LINK)],
            [InlineKeyboardButton("📲 Criar conta BingX", url=BINGX_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "🔐 *Intel Zone (VIP)*\n\n"
            "O ambiente onde você aprende a operar de verdade.\n\n"
            "📊 Análises ao vivo\n"
            "🎯 Entradas e saídas explicadas\n"
            "🎥 Operações em tempo real\n\n"
            "*PASSO A PASSO PARA ENTRAR:*\n\n"
            "1️⃣ Crie sua conta por uma das corretoras abaixo\n"
            "2️⃣ Faça login e copie seu UID\n"
            "3️⃣ Envie o UID aqui para validação\n\n"
            "👉 Após isso, seu acesso será liberado.\n",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    # SINAIS
    elif query.data == "sinais":
        keyboard = [
            [InlineKeyboardButton("⚡ Acessar sinais (10% OFF)", url="https://t.me/aecrypto_bot?start=MAVA")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "⚡ *Grupo de Sinais*\n\n"
            "📈 Operações prontas para execução\n\n"
            "⚠️ Importante:\n"
            "Esses sinais são enviados por um *parceiro externo*.\n"
            "Não são análises feitas por nós.\n\n"
            "👉 Ideal para quem quer praticidade.\n",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    # MENTORIA
    elif query.data == "mentoria":
        keyboard = [
            [InlineKeyboardButton("🎓 Falar com suporte", url=SUPORTE_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "🎓 *Mentoria Wall Street Girls*\n\n"
            "Para quem quer acelerar resultados.\n\n"
            "📈 Acompanhamento próximo\n"
            "🧠 Desenvolvimento de mentalidade\n"
            "🎯 Direcionamento estratégico\n\n"
            "👉 Fale com o suporte:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    # CONTEÚDO
    elif query.data == "conteudo":
        keyboard = [
            [InlineKeyboardButton("▶️ YouTube", url=YOUTUBE_LINK)],
            [InlineKeyboardButton("🎵 TikTok", url=TIKTOK_LINK)],
            [InlineKeyboardButton("📸 Instagram", url=INSTAGRAM_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "📊 *Conteúdo gratuito*\n\n"
            "Acompanhe nossa visão de mercado e estratégias:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    # PAGAMENTO
    elif query.data == "pagamento":
        keyboard = [
            [InlineKeyboardButton("💳 Cobrança avulsa", callback_data="pag_avulso")],
            [InlineKeyboardButton("🔄 Assinatura recorrente", callback_data="pag_recorrente")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "💳 *Pagamentos*\n\n"
            "Escolha o tipo de cobrança:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

    elif query.data == "pag_avulso":
        sessions[chat_id] = {"tipo": "avulso", "etapa": "descricao"}
        await query.message.reply_text(
            "📝 Qual é o nome do produto ou serviço?",
            reply_markup=InlineKeyboardMarkup([[]])
        )

    elif query.data == "pag_recorrente":
        sessions[chat_id] = {"tipo": "recorrente", "etapa": "descricao"}
        await query.message.reply_text(
            "🔄 Qual é o nome do plano ou assinatura?",
            reply_markup=InlineKeyboardMarkup([[]])
        )

    elif query.data in ["per_mensal", "per_semanal", "per_anual"]:
        mapa = {"per_mensal": "monthly", "per_semanal": "weekly", "per_anual": "yearly"}
        session = sessions.get(chat_id, {})
        session["periodicidade"] = mapa[query.data]
        session["etapa"] = "cliente"
        sessions[chat_id] = session
        await query.message.reply_text("👤 Nome do cliente (ou digite *pular*):", parse_mode="Markdown")

# ─── MENSAGENS DE TEXTO (UID + FLUXO DE COBRANÇA) ────────────────────────────
async def processar_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()
    chat_id = update.message.chat_id

    # ── Fluxo de cobrança ────────────────────────────────────────────────────
    session = sessions.get(user_id)
    if session:
        tipo = session["tipo"]
        etapa = session["etapa"]

        if etapa == "descricao":
            session["descricao"] = text
            session["etapa"] = "valor"
            sessions[user_id] = session
            return await update.message.reply_text(
                "💰 Qual é o valor em R$? (ex: `49.90`)",
                parse_mode="Markdown"
            )

        if etapa == "valor":
            try:
                valor = float(text.replace(",", "."))
                if valor <= 0:
                    raise ValueError()
            except ValueError:
                return await update.message.reply_text("⚠️ Valor inválido. Digite novamente (ex: `49.90`):", parse_mode="Markdown")

            session["valor_centavos"] = int(valor * 100)
            sessions[user_id] = session

            if tipo == "recorrente":
                session["etapa"] = "periodicidade"
                keyboard = [
                    [InlineKeyboardButton("📅 Mensal", callback_data="per_mensal")],
                    [InlineKeyboardButton("📅 Semanal", callback_data="per_semanal")],
                    [InlineKeyboardButton("📅 Anual", callback_data="per_anual")]
                ]
                return await update.message.reply_text(
                    "📅 Qual a periodicidade?",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            else:
                session["etapa"] = "cliente"
                sessions[user_id] = session
                return await update.message.reply_text("👤 Nome do cliente (ou digite *pular*):", parse_mode="Markdown")

        if etapa == "cliente":
            cliente_nome = None if text.lower() == "pular" else text
            session["cliente_nome"] = cliente_nome
            sessions.pop(user_id, None)

            await update.message.reply_text("⏳ Gerando link de pagamento...")

            try:
                link = gerar_link_pagamento(
                    descricao=session["descricao"],
                    valor_centavos=session["valor_centavos"],
                    cliente_nome=cliente_nome,
                    recorrente=(tipo == "recorrente"),
                    periodicidade=session.get("periodicidade", "monthly")
                )

                nome_periodo = {"monthly": "Mensal", "weekly": "Semanal", "yearly": "Anual"}
                recorrencia_txt = f"\n📅 *Frequência:* {nome_periodo.get(session.get('periodicidade','monthly'))}" if tipo == "recorrente" else ""
                cliente_txt = f"\n👤 *Cliente:* {cliente_nome}" if cliente_nome else ""

                keyboard = [[InlineKeyboardButton("💳 Pagar agora", url=link)]]
                await update.message.reply_text(
                    f"✅ *Link gerado!*\n\n"
                    f"📦 *Produto:* {session['descricao']}\n"
                    f"💰 *Valor:* {formatar_valor(session['valor_centavos'])}"
                    f"{recorrencia_txt}{cliente_txt}\n\n"
                    f"🔗 Compartilhe o botão abaixo com seu cliente:",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            except Exception as e:
                print("Erro InfinitePay:", e)
                await update.message.reply_text("❌ Erro ao gerar o link. Verifique sua InfiniteTag e tente novamente.")
            return

    # ── Validação de UID (fluxo original) ────────────────────────────────────
    if user_id in aguardando_uid:
        uid = text

        if uid in uids_validos:
            aguardando_uid.remove(user_id)

            keyboard = [[InlineKeyboardButton("🔐 Entrar na Intel Zone", url=VIP_LINK)]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                "✅ *UID validado com sucesso!*\n\n"
                "🔥 Seu acesso está liberado:\n",
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                "❌ UID não encontrado.\n\n"
                "Certifique-se de ter criado conta pelo link correto."
            )

# ─── WEBHOOK INFINITEPAY (Flask em thread separada) ──────────────────────────
flask_app = Flask(__name__)

@flask_app.route("/webhook/infinitepay", methods=["POST"])
def webhook_infinitepay():
    data = flask_request.get_json(silent=True) or {}
    print("Webhook recebido:", data)

    pago = data.get("paid") is True or data.get("status") in ["paid", "approved"]
    if pago and ADMIN_CHAT_ID:
        valor = data.get("paid_amount") or data.get("amount", 0)
        metodo = data.get("capture_method", "—").upper()
        pedido = data.get("order_nsu", "—")
        comprovante = data.get("receipt_url", "")

        mensagem = (
            f"💰 *Pagamento recebido!*\n\n"
            f"💵 *Valor:* {formatar_valor(valor)}\n"
            f"💳 *Método:* {metodo}\n"
            f"🔖 *Pedido:* `{pedido}`"
        )
        if comprovante:
            mensagem += f"\n🧾 [Comprovante]({comprovante})"

        # Envia notificação via API do Telegram
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={"chat_id": ADMIN_CHAT_ID, "text": mensagem, "parse_mode": "Markdown"}
        )

    return "", 200

@flask_app.route("/")
def home():
    return "Bot Wall Street Girls online ✅"

@flask_app.route("/obrigado")
def obrigado():
    return "Pagamento realizado! Obrigado 🎉"

def rodar_flask():
    port = int(os.getenv("PORT", 3000))
    flask_app.run(host="0.0.0.0", port=port)

# ─── RUN ──────────────────────────────────────────────────────────────────────
threading.Thread(target=rodar_flask, daemon=True).start()

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(escolha))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_mensagem))

app.run_polling(){{|
