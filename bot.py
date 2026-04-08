from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os
import json
import datetime

# ──────────────────────────────────────────────
# CONFIGURAÇÕES
# ──────────────────────────────────────────────
TOKEN        = os.getenv("TOKEN")
VIP_GROUP_ID = -1002336704499

INFINITEPAY_LINK = "https://link.infinitepay.io/uppr/VC1DLTEtSQ-1u1nnH5til-49,90"

# ──────────────────────────────────────────────
# LINKS
# ──────────────────────────────────────────────
MEXC_LINK      = "https://promote.mexc.com/b/wallstreetgirls"
BINGX_LINK     = "https://bingx.com/partner/wallstreetgirls"
SUPORTE_LINK   = "https://t.me/suportewsg"
YOUTUBE_LINK   = "https://youtube.com/@wallstreet_girls"
TIKTOK_LINK    = "https://tiktok.com/@wallstreet.girls"
INSTAGRAM_LINK = "https://instagram.com/wallstreet_girls"

# ──────────────────────────────────────────────
# BANCO DE DADOS SIMPLES
# ──────────────────────────────────────────────
DB_FILE = "assinantes.json"

def carregar_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def salvar_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

# ──────────────────────────────────────────────
# ESTADOS
# ──────────────────────────────────────────────
aguardando_uid          = set()
aguardando_comprovante  = set()
uids_validos = ["123456", "789101", "555999"]  # seus UIDs válidos

# ──────────────────────────────────────────────
# /start — menu principal
# ──────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔐 Intel Zone (VIP)", callback_data="vip")],
        [InlineKeyboardButton("⚡ Sinais (parceria)",  callback_data="sinais")],
        [InlineKeyboardButton("🎓 Mentoria",           callback_data="mentoria")],
        [InlineKeyboardButton("📊 Conteúdo gratuito", callback_data="conteudo")],
        [InlineKeyboardButton("💬 Suporte",            url=SUPORTE_LINK)],
    ]
    await update.message.reply_text(
        "💎 *Wall Street Girls*\n\n"
        "Um ecossistema para quem quer operar com estratégia e consistência.\n\n"
        "Aqui você não depende de sorte.\n"
        "Você aprende a ler o mercado.\n\n"
        "👇 Escolha como quer começar:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# ──────────────────────────────────────────────
# CLIQUES
# ──────────────────────────────────────────────
async def escolha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # ── INTEL ZONE VIP — 3 formas ───────────────
    if query.data == "vip":
        keyboard = [
            [InlineKeyboardButton("1️⃣ Criar conta MEXC (gratuito)",           url=MEXC_LINK)],
            [InlineKeyboardButton("2️⃣ Criar conta BingX (gratuito)",          url=BINGX_LINK)],
            [InlineKeyboardButton("✅ Já criei minha conta — enviar UID",      callback_data="validar_uid")],
            [InlineKeyboardButton("3️⃣ Assinar por R$49,90/mês 💳",           callback_data="pagar_vip")],
        ]
        await query.message.reply_text(
            "🔐 *Intel Zone VIP*\n\n"
            "O ambiente onde você aprende a operar de verdade.\n\n"
            "📊 Análises ao vivo\n"
            "🎯 Entradas e saídas explicadas\n"
            "🎥 Operações em tempo real\n"
            "💬 Comunidade exclusiva\n\n"
            "─────────────────────\n"
            "🟡 *3 formas de entrar:*\n\n"
            "1️⃣ *MEXC — gratuito*\n"
            "Crie sua conta pelo nosso link. O acesso ao VIP é liberado automaticamente, sem custo extra pra você. A corretora nos repassa uma comissão.\n\n"
            "2️⃣ *BingX — gratuito*\n"
            "Mesma coisa pela BingX. Crie pelo nosso link e ganhe acesso completo incluído.\n\n"
            "3️⃣ *Assinatura — R$49,90/mês*\n"
            "Prefere usar outra corretora ou já tem conta? Assine diretamente via PIX ou cartão. Renovação todo mês, cancele quando quiser.\n\n"
            "─────────────────────\n"
            "👇 Escolha sua forma de acesso:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # ── VALIDAR UID (corretoras) ─────────────────
    elif query.data == "validar_uid":
        aguardando_uid.add(query.from_user.id)
        await query.message.reply_text(
            "✅ Ótimo!\n\n"
            "Agora envie aqui o seu *UID* da corretora para validarmos seu acesso.\n\n"
            "_O UID fica no seu perfil dentro da corretora._",
            parse_mode="Markdown",
        )

    # ── PAGAR R$49,90 VIA INFINITEPAY ────────────
    elif query.data == "pagar_vip":
        aguardando_comprovante.add(query.from_user.id)
        keyboard = [
            [InlineKeyboardButton("💳 Pagar agora (PIX ou cartão)", url=INFINITEPAY_LINK)],
        ]
        await query.message.reply_text(
            "💳 *Assinatura Intel Zone VIP*\n\n"
            "💰 R$49,90/mês\n"
            "🔄 Renovação todo mês\n"
            "❌ Cancele quando quiser\n\n"
            "✅ *Incluso:*\n"
            "• Análises ao vivo\n"
            "• Entradas e saídas explicadas\n"
            "• Operações em tempo real\n"
            "• Comunidade exclusiva\n\n"
            "👇 *Passo a passo:*\n"
            "1️⃣ Clique no botão abaixo e efetue o pagamento\n"
            "2️⃣ Após pagar, envie o *comprovante aqui* nesta conversa\n"
            "3️⃣ Vamos validar e liberar seu acesso em até 24h ⏳\n",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # ── SINAIS ───────────────────────────────────
    elif query.data == "sinais":
        keyboard = [[InlineKeyboardButton("⚡ Acessar sinais (10% OFF)", url="https://t.me/aecrypto_bot?start=MAVA")]]
        await query.message.reply_text(
            "⚡ *Grupo de Sinais*\n\n"
            "📈 Operações prontas para execução\n\n"
            "⚠️ Importante:\n"
            "Esses sinais são enviados por um *parceiro externo*.\n"
            "Não são análises feitas por nós.\n\n"
            "👉 Ideal para quem quer praticidade.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # ── MENTORIA ─────────────────────────────────
    elif query.data == "mentoria":
        keyboard = [[InlineKeyboardButton("🎓 Falar com suporte", url=SUPORTE_LINK)]]
        await query.message.reply_text(
            "🎓 *Mentoria Wall Street Girls*\n\n"
            "Para quem quer acelerar resultados.\n\n"
            "📈 Acompanhamento próximo\n"
            "🧠 Desenvolvimento de mentalidade\n"
            "🎯 Direcionamento estratégico\n\n"
            "👉 Fale com o suporte:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # ── CONTEÚDO ─────────────────────────────────
    elif query.data == "conteudo":
        keyboard = [
            [InlineKeyboardButton("▶️ YouTube",   url=YOUTUBE_LINK)],
            [InlineKeyboardButton("🎵 TikTok",    url=TIKTOK_LINK)],
            [InlineKeyboardButton("📸 Instagram", url=INSTAGRAM_LINK)],
        ]
        await query.message.reply_text(
            "📊 *Conteúdo gratuito*\n\n"
            "Acompanhe nossa visão de mercado e estratégias:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # ── LIBERAR ACESSO (admin) ───────────────────
    elif query.data.startswith("liberar_"):
        target_id = int(query.data.split("_")[1])
        try:
            link = await context.bot.create_chat_invite_link(
                chat_id=VIP_GROUP_ID,
                member_limit=1,
                expire_date=datetime.datetime.now() + datetime.timedelta(hours=24),
            )
            db = carregar_db()
            db[str(target_id)] = {
                "ativo": True,
                "pago_em": datetime.datetime.now().isoformat(),
                "renovar_em": (datetime.datetime.now() + datetime.timedelta(days=30)).isoformat(),
            }
            salvar_db(db)
            await context.bot.send_message(
                chat_id=target_id,
                text=(
                    "✅ *Pagamento confirmado!*\n\n"
                    "🔥 Bem-vinda à *Intel Zone VIP*!\n\n"
                    "👇 Use o link abaixo para entrar no canal:\n"
                    f"{link.invite_link}\n\n"
                    "⚠️ O link é de uso único e expira em 24h.\n\n"
                    "Qualquer dúvida: @suportewsg"
                ),
                parse_mode="Markdown"
            )
            await query.message.reply_text(f"✅ Acesso liberado para o usuário `{target_id}`!", parse_mode="Markdown")
        except Exception as e:
            await query.message.reply_text(f"❌ Erro ao liberar acesso: {e}")

    # ── RECUSAR (admin) ──────────────────────────
    elif query.data.startswith("recusar_"):
        target_id = int(query.data.split("_")[1])
        await context.bot.send_message(
            chat_id=target_id,
            text=(
                "❌ *Comprovante não aprovado*\n\n"
                "Não conseguimos validar seu pagamento.\n\n"
                "Por favor, envie o comprovante correto ou fale com o suporte: @suportewsg"
            ),
            parse_mode="Markdown"
        )
        await query.message.reply_text(f"❌ Comprovante recusado para `{target_id}`.", parse_mode="Markdown")

# ──────────────────────────────────────────────
# MENSAGENS DE TEXTO E IMAGENS
# ──────────────────────────────────────────────
async def receber_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id

    # Validação de UID
    if user_id in aguardando_uid:
        uid = update.message.text.strip()
        if uid in uids_validos:
            aguardando_uid.remove(user_id)
            keyboard = [[InlineKeyboardButton("🔐 Entrar na Intel Zone", url="https://t.me/+KN3vIstR8B1kZjEx")]]
            await update.message.reply_text(
                "✅ *UID validado com sucesso!*\n\n"
                "🔥 Seu acesso está liberado:",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        else:
            await update.message.reply_text(
                "❌ UID não encontrado.\n\n"
                "Certifique-se de ter criado a conta pelo nosso link.\n"
                "Dúvidas? Fale com o suporte: @suportewsg"
            )
        return

    # Comprovante de pagamento (texto ou imagem)
    if user_id in aguardando_comprovante:
        aguardando_comprovante.discard(user_id)
        nome = user.full_name
        username = f"@{user.username}" if user.username else "sem username"

        # Avisa o admin (você) para aprovar ou recusar
        ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # coloque seu ID pessoal no Railway
        keyboard = [
            [
                InlineKeyboardButton("✅ Liberar acesso", callback_data=f"liberar_{user_id}"),
                InlineKeyboardButton("❌ Recusar",        callback_data=f"recusar_{user_id}"),
            ]
        ]
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"💳 *Novo comprovante recebido!*\n\n"
                f"👤 Nome: {nome}\n"
                f"🔗 Username: {username}\n"
                f"🆔 ID: `{user_id}`\n\n"
                f"Clique para liberar ou recusar o acesso:"
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        # Encaminha o comprovante para o admin
        await update.message.forward(chat_id=ADMIN_ID)

        await update.message.reply_text(
            "✅ *Comprovante recebido!*\n\n"
            "Vamos validar e liberar seu acesso em até 24h. 🕐\n\n"
            "Qualquer dúvida: @suportewsg",
            parse_mode="Markdown"
        )

# ──────────────────────────────────────────────
# RECEBER IMAGENS (comprovante em foto)
# ──────────────────────────────────────────────
async def receber_foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id

    if user_id in aguardando_comprovante:
        aguardando_comprovante.discard(user_id)
        nome = user.full_name
        username = f"@{user.username}" if user.username else "sem username"

        ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
        keyboard = [
            [
                InlineKeyboardButton("✅ Liberar acesso", callback_data=f"liberar_{user_id}"),
                InlineKeyboardButton("❌ Recusar",        callback_data=f"recusar_{user_id}"),
            ]
        ]
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"💳 *Novo comprovante recebido!*\n\n"
                f"👤 Nome: {nome}\n"
                f"🔗 Username: {username}\n"
                f"🆔 ID: `{user_id}`\n\n"
                f"Clique para liberar ou recusar o acesso:"
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        await update.message.forward(chat_id=ADMIN_ID)

        await update.message.reply_text(
            "✅ *Comprovante recebido!*\n\n"
            "Vamos validar e liberar seu acesso em até 24h. 🕐\n\n"
            "Qualquer dúvida: @suportewsg",
            parse_mode="Markdown"
        )

# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(escolha))
    app.add_handler(MessageHandler(filters.PHOTO, receber_foto))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receber_mensagem))
    app.run_polling()

if __name__ == "__main__":
    main()
