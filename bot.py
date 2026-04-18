from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os
import json
import datetime

TOKEN        = os.getenv("TOKEN")
VIP_GROUP_ID = -1002336704499
ADMIN_ID     = 5908958242

INFINITEPAY_LINK = "https://link.infinitepay.io/uppr/VC1DLTEtSQ-lcpUeOVNl-79,90"

SUPORTE_LINK   = "https://t.me/suportewsg"
YOUTUBE_LINK   = "https://youtube.com/@wallstreet_girls"
TIKTOK_LINK    = "https://tiktok.com/@wallstreet.girls"
INSTAGRAM_LINK = "https://instagram.com/wallstreet_girls"

DB_FILE = "assinantes.json"

def carregar_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def salvar_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

aguardando_comprovante = set()

async def registrar_e_notificar(context, user_id, nome, username, via):
    link_obj = await context.bot.create_chat_invite_link(
        chat_id=VIP_GROUP_ID,
        member_limit=1,
        expire_date=datetime.datetime.now() + datetime.timedelta(hours=48),
    )
    link = link_obj.invite_link

    db = carregar_db()
    db[str(user_id)] = {
        "ativo": True,
        "nome": nome,
        "username": username,
        "via": via,
        "entrou_em": datetime.datetime.now().isoformat(),
        "renovar_em": (datetime.datetime.now() + datetime.timedelta(days=30)).isoformat(),
    }
    salvar_db(db)

    await context.bot.send_message(
        chat_id=user_id,
        text=(
            "✅ *Acesso liberado!*\n\n"
            "🔥 Bem-vindo(a) ao *Intel Zone*!\n\n"
            "👇 Clique no link abaixo para entrar:\n"
            + link + "\n\n"
            "⚠️ O link é de uso único e expira em 48h.\n"
            "Não compartilhe com ninguém!\n\n"
            "Qualquer dúvida: @suportewsg"
        ),
        parse_mode="Markdown"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            "🟢 *Novo membro - Intel Zone!*\n\n"
            "👤 Nome: " + nome + "\n"
            "🔗 Username: " + username + "\n"
            "🆔 ID: " + str(user_id) + "\n"
            "📥 Via: " + via + "\n"
            "📅 " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        ),
    )

async def enviar_para_suporte(context, user_id, nome, username, via, mensagem_extra=""):
    db = carregar_db()
    db[str(user_id)] = db.get(str(user_id), {})
    db[str(user_id)]["nome"]     = nome
    db[str(user_id)]["username"] = username
    db[str(user_id)]["ativo"]    = False
    salvar_db(db)

    keyboard = [[
        InlineKeyboardButton("✅ Liberar acesso", callback_data="liberar_" + str(user_id)),
        InlineKeyboardButton("❌ Recusar", callback_data="recusar_" + str(user_id)),
    ]]
    texto = (
        "📋 Nova solicitação de acesso!\n\n"
        "👤 Nome: " + nome + "\n"
        "🔗 Username: " + username + "\n"
        "🆔 ID: " + str(user_id) + "\n"
        "📥 Via: " + via + "\n"
    )
    if mensagem_extra:
        texto += "📝 Info: " + mensagem_extra + "\n"
    texto += "\n👇 Verifique e libere o acesso:"

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=texto,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💎 Intel Zone — Análises e Ideias de Trade", callback_data="vip")],
        [InlineKeyboardButton("📊 Conteúdo gratuito", callback_data="conteudo")],
        [InlineKeyboardButton("🎓 Mentoria", callback_data="mentoria")],
        [InlineKeyboardButton("✅ Enviar comprovante", callback_data="pagar_vip")],
        [InlineKeyboardButton("💬 Suporte", url=SUPORTE_LINK)],
    ]
    await update.message.reply_text(
        "👑 *Wall Street Girls*\n\n"
        "Um ecossistema para quem quer operar com estratégia e consistência.\n\n"
        "Aqui você não depende de sorte.\n"
        "Você aprende a ler o mercado.\n\n"
        "─────────────────────\n"
        "🟡 *Quer entrar no Intel Zone?*\n"
        "Nosso grupo premium de análises e ideias de trade.\n\n"
        "1️⃣ Clique em *Intel Zone* para saber mais\n"
        "2️⃣ Efetue o pagamento de R$79,90/mês\n"
        "3️⃣ Volte aqui e clique em *Enviar comprovante*\n"
        "4️⃣ A gente valida e manda o link do grupo pra você! ✅\n\n"
        "─────────────────────\n"
        "👇 Escolha como quer começar:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def escolha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "vip":
        keyboard = [
            [InlineKeyboardButton("💳 Assinar por R$79,90/mês", callback_data="pagar_vip")],
        ]
        await query.message.reply_text(
            "💎 *Intel Zone — análises e ideias de trade*\n\n"
            "Aqui você não recebe sinal de terceiro.\n"
            "Você acompanha *a gente analisando o mercado ao vivo.*\n\n"
            "Cada análise explicada. Cada ideia justificada.\n"
            "Você aprende enquanto opera.\n\n"
            "✅ *O que você encontra aqui:*\n"
            "📊 Análises técnicas feitas por nós\n"
            "💡 Ideias de trade com explicação completa\n"
            "🧠 Raciocínio por trás de cada decisão\n"
            "💬 Comunidade exclusiva de traders\n\n"
            "─────────────────────\n"
            "💰 *R$79,90/mês* — recorrência no cartão\n\n"
            "🎁 *Bônus:* ao assinar você ganha 7 dias grátis de acesso ao *Intel Zone LT* "
            "— operações ao vivo em tempo real!\n\n"
            "─────────────────────\n"
            "👇 Clique abaixo para assinar:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "pagar_vip":
        aguardando_comprovante.add(query.from_user.id)
        keyboard = [[InlineKeyboardButton("💳 Pagar agora (PIX ou cartão)", url=INFINITEPAY_LINK)]]
        await query.message.reply_text(
            "📋 *Enviar comprovante — acesso ao Intel Zone*\n\n"
            "💳 Assine por *R$79,90/mês* clicando no botão abaixo.\n\n"
            "Após o pagamento, envie o comprovante aqui (foto ou texto) "
            "que a gente valida e manda o link do grupo pra você! ✅\n\n"
            "⚠️ Não feche essa conversa. Volte aqui e envie o comprovante.\n\n"
            "Qualquer dúvida: @suportewsg",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data.startswith("liberar_"):
        target_id = int(query.data.split("_")[1])
        db = carregar_db()
        dados    = db.get(str(target_id), {})
        nome     = dados.get("nome", str(target_id))
        username = dados.get("username", "-")
        via      = dados.get("via", "-")
        try:
            await registrar_e_notificar(context, target_id, nome, username, via)
            await query.message.reply_text("✅ Acesso liberado para " + nome + "!")
        except Exception as e:
            await query.message.reply_text("❌ Erro: " + str(e))

    elif query.data.startswith("recusar_"):
        target_id = int(query.data.split("_")[1])
        await context.bot.send_message(
            chat_id=target_id,
            text=(
                "❌ *Não conseguimos validar seu acesso.*\n\n"
                "Pode ter acontecido um desses casos:\n"
                "• O comprovante não foi identificado\n"
                "• O pagamento não foi confirmado\n\n"
                "Fale com o suporte e a gente resolve rápido: @suportewsg"
            ),
            parse_mode="Markdown"
        )
        await query.message.reply_text("❌ Solicitação recusada.")

    elif query.data == "mentoria":
        keyboard = [[InlineKeyboardButton("🎓 Falar com suporte", url=SUPORTE_LINK)]]
        await query.message.reply_text(
            "🎓 *Mentoria Wall Street Girls*\n\n"
            "Para quem quer acelerar resultados.\n\n"
            "📈 Acompanhamento próximo\n"
            "🧠 Desenvolvimento de mentalidade\n"
            "🎯 Direcionamento estratégico\n\n"
            "👉 Fale com o suporte para saber mais:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "conteudo":
        keyboard = [
            [InlineKeyboardButton("▶️ YouTube", url=YOUTUBE_LINK)],
            [InlineKeyboardButton("🎵 TikTok", url=TIKTOK_LINK)],
            [InlineKeyboardButton("📸 Instagram", url=INSTAGRAM_LINK)],
        ]
        await query.message.reply_text(
            "📊 *Conteúdo gratuito*\n\n"
            "Acompanhe nossa visão de mercado e estratégias:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

async def receber_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user     = update.message.from_user
    user_id  = user.id
    nome     = user.full_name
    username = "@" + user.username if user.username else "sem username"

    if user_id in aguardando_comprovante:
        aguardando_comprovante.discard(user_id)
        db = carregar_db()
        db[str(user_id)] = db.get(str(user_id), {})
        db[str(user_id)]["nome"]     = nome
        db[str(user_id)]["username"] = username
        db[str(user_id)]["ativo"]    = False
        db[str(user_id)]["via"]      = "Pagamento R$79,90"
        salvar_db(db)

        await enviar_para_suporte(context, user_id, nome, username, "Pagamento R$79,90")
        await update.message.forward(chat_id=ADMIN_ID)
        await update.message.reply_text(
            "✅ *Comprovante recebido!*\n\n"
            "Estamos verificando e vamos liberar seu acesso em breve. 🕐\n\n"
            "Qualquer dúvida: @suportewsg",
        )

async def receber_foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user     = update.message.from_user
    user_id  = user.id
    nome     = user.full_name
    username = "@" + user.username if user.username else "sem username"

    if user_id in aguardando_comprovante:
        aguardando_comprovante.discard(user_id)
        db = carregar_db()
        db[str(user_id)] = db.get(str(user_id), {})
        db[str(user_id)]["nome"]     = nome
        db[str(user_id)]["username"] = username
        db[str(user_id)]["ativo"]    = False
        db[str(user_id)]["via"]      = "Pagamento R$79,90"
        salvar_db(db)

        await enviar_para_suporte(context, user_id, nome, username, "Pagamento R$79,90")
        await update.message.forward(chat_id=ADMIN_ID)
        await update.message.reply_text(
            "✅ *Comprovante recebido!*\n\n"
            "Estamos verificando e vamos liberar seu acesso em breve. 🕐\n\n"
            "Qualquer dúvida: @suportewsg",
        )

async def listar_membros(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return
    db = carregar_db()
    if not db:
        await update.message.reply_text("Nenhum membro registrado ainda.")
        return
    texto = "📋 *Membros registrados:*\n\n"
    for i, (uid, dados) in enumerate(db.items(), 1):
        nome     = dados.get("nome", "-")
        username = dados.get("username", "-")
        entrou   = dados.get("entrou_em", "-")
        grupo    = dados.get("grupo", "-")
        ativo    = "✅ Ativo" if dados.get("ativo") else "⏳ Pendente"
        texto += f"{i}. *{nome}* ({username})\n🆔 {uid} | {ativo}\n📅 {entrou} | {grupo}\n\n"
        if len(texto) > 3500:
            await update.message.reply_text(texto, parse_mode="Markdown")
            texto = ""
    if texto:
        await update.message.reply_text(texto, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("membros", listar_membros))
    app.add_handler(CallbackQueryHandler(escolha))
    app.add_handler(MessageHandler(filters.PHOTO, receber_foto))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receber_texto))
    app.run_polling()

if __name__ == "__main__":
    main()
