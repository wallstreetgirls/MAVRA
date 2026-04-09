from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os
import json
import datetime

TOKEN        = os.getenv("TOKEN")
VIP_GROUP_ID = -1002336704499
ADMIN_ID     = 8671065515

INFINITEPAY_LINK = "https://link.infinitepay.io/uppr/VC1DLTEtSQ-1u1nnH5til-49,90"

MEXC_LINK      = "https://promote.mexc.com/b/wallstreetgirls"
BINGX_LINK     = "https://bingx.com/partner/wallstreetgirls"
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

aguardando_uid         = set()
aguardando_comprovante = set()
uids_validos = ["123456", "789101", "555999"]

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
            "🔥 Bem-vinda ao *Crypto Intel Zone*!\n\n"
            "👇 Clique no link abaixo para entrar:\n"
            + link + "\n\n"
            "⚠️ O link e de uso unico e expira em 48h.\n"
            "Nao compartilhe com ninguem!\n\n"
            "Qualquer duvida: @suportewsg"
        ),
        parse_mode="Markdown"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            "🟢 *Novo membro - Crypto Intel Zone!*\n\n"
            "👤 Nome: " + nome + "\n"
            "🔗 Username: " + username + "\n"
            "🆔 ID: " + str(user_id) + "\n"
            "📥 Via: " + via + "\n"
            "📅 " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        ),
        parse_mode="Markdown"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔐 Crypto Intel Zone (VIP)", callback_data="vip")],
        [InlineKeyboardButton("⚡ Sinais AE Crypto", callback_data="sinais")],
        [InlineKeyboardButton("🎓 Mentoria", callback_data="mentoria")],
        [InlineKeyboardButton("📊 Conteudo gratuito", callback_data="conteudo")],
        [InlineKeyboardButton("💬 Suporte", url=SUPORTE_LINK)],
    ]
    await update.message.reply_text(
        "💎 *Wall Street Girls*\n\n"
        "Um ecossistema para quem quer operar com estrategia e consistencia.\n\n"
        "Aqui voce nao depende de sorte.\n"
        "Voce aprende a ler o mercado.\n\n"
        "👇 Escolha como quer comecar:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def escolha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "vip":
        keyboard = [
            [InlineKeyboardButton("1️⃣ Criar conta MEXC (gratuito)", url=MEXC_LINK)],
            [InlineKeyboardButton("2️⃣ Criar conta BingX (gratuito)", url=BINGX_LINK)],
            [InlineKeyboardButton("✅ Ja criei minha conta - enviar UID", callback_data="validar_uid")],
            [InlineKeyboardButton("3️⃣ Assinar por R$49,90/mes 💳", callback_data="pagar_vip")],
        ]
        await query.message.reply_text(
            "🔐 *Crypto Intel Zone - nosso canal VIP*\n\n"
            "Aqui voce acompanha nossas analises, entradas e saidas em tempo real. "
            "Tudo explicado, operacao por operacao.\n\n"
            "📊 Analises ao vivo\n"
            "🎯 Entradas e saidas explicadas\n"
            "🎥 Operacoes em tempo real\n"
            "💬 Comunidade exclusiva\n\n"
            "─────────────────────\n"
            "🟡 *3 formas de entrar:*\n\n"
            "1️⃣ *MEXC - gratuito*\n"
            "Crie sua conta pelo nosso link. Apos criar, volte aqui, clique em "
            "*Ja criei minha conta* e envie seu UID para liberar o acesso.\n\n"
            "2️⃣ *BingX - gratuito*\n"
            "Mesma coisa pela BingX. Crie pelo nosso link, volte aqui, clique em "
            "*Ja criei minha conta* e envie seu UID.\n\n"
            "3️⃣ *Assinatura - R$49,90/mes*\n"
            "Prefere usar outra corretora ou ja tem conta? Assine diretamente. "
            "Apos o pagamento, volte aqui e envie o comprovante para liberar o acesso.\n\n"
            "─────────────────────\n"
            "👇 Escolha sua forma de acesso:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "validar_uid":
        aguardando_uid.add(query.from_user.id)
        await query.message.reply_text(
            "✅ *Otimo!*\n\n"
            "Agora envie aqui o seu *UID* da corretora para validarmos seu acesso.\n\n"
            "📌 *Como encontrar seu UID:*\n"
            "Abra o app da corretora, clique na sua foto de perfil. O UID aparece abaixo do seu nome.\n\n"
            "Assim que validarmos, voce recebe o link do canal aqui mesmo.",
            parse_mode="Markdown",
        )

    elif query.data == "pagar_vip":
        aguardando_comprovante.add(query.from_user.id)
        keyboard = [[InlineKeyboardButton("💳 Pagar agora (PIX ou cartao)", url=INFINITEPAY_LINK)]]
        await query.message.reply_text(
            "💳 *Assinatura Crypto Intel Zone - R$49,90/mes*\n\n"
            "📌 *Passo a passo:*\n\n"
            "1️⃣ Clique no botao abaixo e efetue o pagamento\n"
            "2️⃣ Apos pagar, volte aqui e envie o comprovante (foto ou texto)\n"
            "3️⃣ Assim que validarmos, voce recebe o link do canal aqui mesmo ✅\n\n"
            "⚠️ Nao feche essa conversa apos pagar. "
            "Volte aqui e envie o comprovante para liberar seu acesso.\n\n"
            "🔄 Renovacao todo mes\n"
            "❌ Cancele quando quiser",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data.startswith("liberar_"):
        target_id = int(query.data.split("_")[1])
        db = carregar_db()
        dados    = db.get(str(target_id), {})
        nome     = dados.get("nome", str(target_id))
        username = dados.get("username", "-")
        try:
            await registrar_e_notificar(context, target_id, nome, username, "Infinitepay")
            await query.message.reply_text("✅ Acesso liberado para " + nome + "!")
        except Exception as e:
            await query.message.reply_text("❌ Erro: " + str(e))

    elif query.data.startswith("recusar_"):
        target_id = int(query.data.split("_")[1])
        await context.bot.send_message(
            chat_id=target_id,
            text=(
                "❌ *Comprovante nao aprovado*\n\n"
                "Nao conseguimos validar seu pagamento.\n\n"
                "Envie o comprovante correto ou fale com o suporte: @suportewsg"
            ),
            parse_mode="Markdown"
        )
        await query.message.reply_text("❌ Comprovante recusado.")

    elif query.data == "sinais":
        keyboard = [[InlineKeyboardButton("⚡ Acessar sinais AE Crypto (10% OFF)", url="https://t.me/aecrypto_bot?start=MAVA")]]
        await query.message.reply_text(
            "⚡ *Sinais AE Crypto*\n\n"
            "Este e um servico do grupo *AE Crypto*, nosso parceiro.\n\n"
            "📈 Sinais prontos para execucao, enviados diretamente pelo time deles.\n\n"
            "⚠️ *Atencao:* esses sinais *nao sao* do Wall Street Girls. "
            "Sao operacoes do AE Crypto, disponibilizadas aqui com desconto exclusivo para nossa comunidade.\n\n"
            "👉 Ideal para quem quer praticidade e operacoes prontas.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "mentoria":
        keyboard = [[InlineKeyboardButton("🎓 Falar com suporte", url=SUPORTE_LINK)]]
        await query.message.reply_text(
            "🎓 *Mentoria Wall Street Girls*\n\n"
            "Para quem quer acelerar resultados.\n\n"
            "📈 Acompanhamento proximo\n"
            "🧠 Desenvolvimento de mentalidade\n"
            "🎯 Direcionamento estrategico\n\n"
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
            "📊 *Conteudo gratuito*\n\n"
            "Acompanhe nossa visao de mercado e estrategias:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

async def receber_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user     = update.message.from_user
    user_id  = user.id
    nome     = user.full_name
    username = "@" + user.username if user.username else "sem username"

    if user_id in aguardando_uid:
        uid = update.message.text.strip()
        if uid in uids_validos:
            aguardando_uid.discard(user_id)
            await registrar_e_notificar(context, user_id, nome, username, "Corretora (UID)")
        else:
            await update.message.reply_text(
                "❌ *UID nao encontrado.*\n\n"
                "Certifique-se de ter criado a conta pelo nosso link e que copiou o UID corretamente.\n\n"
                "Duvidas? Fale com o suporte: @suportewsg",
                parse_mode="Markdown"
            )
        return

    if user_id in aguardando_comprovante:
        aguardando_comprovante.discard(user_id)
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
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                "💳 *Novo comprovante recebido!*\n\n"
                "👤 Nome: " + nome + "\n"
                "🔗 Username: " + username + "\n"
                "🆔 ID: " + str(user_id) + "\n\n"
                "👇 Verifique e libere o acesso:"
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        await update.message.forward(chat_id=ADMIN_ID)
        await update.message.reply_text(
            "✅ *Comprovante recebido!*\n\n"
            "Estamos verificando e vamos liberar seu acesso em breve.\n\n"
            "Qualquer duvida: @suportewsg",
            parse_mode="Markdown"
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
        salvar_db(db)

        keyboard = [[
            InlineKeyboardButton("✅ Liberar acesso", callback_data="liberar_" + str(user_id)),
            InlineKeyboardButton("❌ Recusar", callback_data="recusar_" + str(user_id)),
        ]]
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                "💳 *Novo comprovante recebido!*\n\n"
                "👤 Nome: " + nome + "\n"
                "🔗 Username: " + username + "\n"
                "🆔 ID: " + str(user_id) + "\n\n"
                "👇 Verifique e libere o acesso:"
            ),
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        await update.message.forward(chat_id=ADMIN_ID)
        await update.message.reply_text(
            "✅ *Comprovante recebido!*\n\n"
            "Estamos verificando e vamos liberar seu acesso em breve.\n\n"
            "Qualquer duvida: @suportewsg",
            parse_mode="Markdown"
        )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(escolha))
    app.add_handler(MessageHandler(filters.PHOTO, receber_foto))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receber_texto))
    app.run_polling()

if __name__ == "__main__":
    main()
