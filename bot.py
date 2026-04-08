from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

import os
TOKEN = os.getenv("TOKEN")
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

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔐 Intel Zone (VIP)", callback_data="vip")],
        [InlineKeyboardButton("⚡ Sinais (parceria)", callback_data="sinais")],
        [InlineKeyboardButton("🎓 Mentoria", callback_data="mentoria")],
        [InlineKeyboardButton("📊 Conteúdo gratuito", callback_data="conteudo")],
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

# CLIQUES
async def escolha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # VIP
    if query.data == "vip":
        aguardando_uid.add(query.from_user.id)

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

# UID
async def validar_uid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id in aguardando_uid:
        uid = update.message.text.strip()

        if uid in uids_validos:
            aguardando_uid.remove(user_id)

            keyboard = [
                [InlineKeyboardButton("🔐 Entrar na Intel Zone", url=VIP_LINK)]
            ]
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

# RUN
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(escolha))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, validar_uid))

app.run_polling()
