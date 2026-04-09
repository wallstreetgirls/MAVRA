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
            "Não compartilhe com ninguem!\n\n"
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
        "📋 Nova solicitacao de acesso!\n\n"
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
        [InlineKeyboardButton("💎 Crypto Intel Zone — Análises e Operações", callback_data="vip")],
        [InlineKeyboardButton("📊 Conteúdo gratuito", callback_data="conteudo")],
        [InlineKeyboardButton("🎓 Mentoria", callback_data="mentoria")],
        [InlineKeyboardButton("🤝 Parceiro Externo — AE Crypto", callback_data="sinais")],
        [InlineKeyboardButton("✅ Enviar comprovante", callback_data="pagar_vip")],
        [InlineKeyboardButton("💬 Suporte", url=SUPORTE_LINK)],
    ]
    await update.message.reply_text(
        "💎 *Wall Street Girls*\n\n"
        "Um ecossistema para quem quer operar com estratégia e consistência.\n\n"
        "Aqui você não depende de sorte.\n"
        "Você aprende a ler o mercado.\n\n"
        "─────────────────────\n"
        "🟡 *Quer entrar no Crypto Intel Zone?*\n"
        "Nosso grupo premium de análises e operações ao vivo.\n\n"
        "1️⃣ Clique em *Crypto Intel Zone* e escolha sua forma de acesso\n"
        "2️⃣ Crie sua conta na corretora parceira ou efetue o pagamento\n"
        "3️⃣ Retorne ao bot e selecione *✅ Enviar comprovante*\n"
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
            [InlineKeyboardButton("1️⃣ Criar conta MEXC (gratuito)", url=MEXC_LINK)],
            [InlineKeyboardButton("2️⃣ Criar conta BingX (gratuito)", url=BINGX_LINK)],
            [InlineKeyboardButton("3️⃣ Assinar por R$49,90/mês 💳", callback_data="pagar_vip")],
            [InlineKeyboardButton("✅ Enviar comprovante", callback_data="pagar_vip")],
        ]
        await query.message.reply_text(
            "💎 *Crypto Intel Zone — grupo premium de analises e operacoes*\n\n"
            "Aqui você não recebe sinal de terceiro.\n"
            "Você acompanha *a gente operando ao vivo.*\n\n"
            "Cada entrada explicada. Cada saida justificada.\n"
            "Você aprende enquanto lucra.\n\n"
            "✅ *O que você encontra aqui:*\n"
            "📊 Análises técnicas feitas por nos\n"
            "🎯 Entradas e saídas com explicação completa\n"
            "🎥 Operações ao vivo em tempo real\n"
            "🧠 Raciocínio por tras de cada decisão\n"
            "💬 Comunidade exclusiva de traders\n\n"
            "Não é sinal pronto para copiar.\n"
            "E voce entendendo o mercado de verdade.\n\n"
            "─────────────────────\n"
            "🟡 *3 formas de entrar:*\n\n"
            "1️⃣ *MEXC - gratuito*\n"
            "Crie sua conta pelo nosso link. Apos criar, volte ao menu principal e clique em "
            "*Enviar comprovante* para enviar seu UID e liberar o acesso.\n\n"
            "2️⃣ *BingX - gratuito*\n"
            "Mesma coisa pela BingX. Crie pelo nosso link, volte ao menu principal e clique em "
            "*Enviar comprovante* para enviar seu UID.\n\n"
            "3️⃣ *Assinatura - R$49,90/mes*\n"
            "Ja tem corretora ou prefere assinar direto? Clique abaixo, efetue o pagamento e "
            "envie o comprovante pelo menu principal para liberar o acesso.\n\n"
            "─────────────────────\n"
            "👇 Escolha sua forma de acesso:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
 
    elif query.data == "validar_uid":
        aguardando_uid.add(query.from_user.id)
        await query.message.reply_text(
            "✅ *Ótimo!*\n\n"
            "Agora envie aqui o seu *UID* da corretora.\n\n"
            "📌 *Como encontrar seu UID:*\n"
            "Abra o app da corretora, clique na sua foto de perfil. "
            "O UID aparece abaixo do seu nome.\n\n"
            "So enviar o numero aqui que a gente valida e libera seu acesso! 👇",
            parse_mode="Markdown",
        )
 
    elif query.data == "pagar_vip":
        aguardando_comprovante.add(query.from_user.id)
        keyboard = [[InlineKeyboardButton("💳 Pagar agora (PIX ou cartao)", url=INFINITEPAY_LINK)]]
        await query.message.reply_text(
            "📋 *Enviar comprovante — acesso ao grupo premium*\n\n"
            "Escolha sua situação:\n\n"
            "🏦 *Criou conta na MEXC ou BingX pelo nosso link?*\n"
            "Envie aqui o seu UID (numero do seu perfil na corretora).\n\n"
            "💳 *Quer assinar por R$49,90/mes?*\n"
            "Clique no botao abaixo para pagar, depois envie o comprovante aqui (foto ou texto).\n\n"
            "⚠️ Não feche essa conversa. Volte aqui e envie o UID ou comprovante para liberar seu acesso.\n\n"
            "A gente valida e manda o link do grupo pra voce! ✅",
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
                "• O UID não foi criado pelo nosso link\n"
                "• O comprovante não foi identificado\n\n"
                "Fale com o suporte e a gente resolve rapido: @suportewsg"
            ),
            parse_mode="Markdown"
        )
        await query.message.reply_text("❌ Solicitação recusada.")
 
    elif query.data == "sinais":
        keyboard = [[InlineKeyboardButton("⚡ Acessar sinais AE Crypto (10% OFF)", url="https://t.me/aecrypto_bot?start=MAVA")]]
        await query.message.reply_text(
            "⚡ *Sinais AE Crypto*\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "⚠️ *Atenção: este servico NAO e do Wall Street Girls.*\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Os sinais sao enviados pelo grupo *AE Crypto*, nosso parceiro externo. "
            "Sao operações prontas para copiar, sem explicação de raciocínio.\n\n"
            "👉 Disponibilizamos aqui porque e um parceiro de confianca e "
            "nossa comunidade ganha *10% de desconto* no acesso.\n\n"
            "Se você quer entender o mercado e acompanhar operações explicadas por nos, "
            "acesse o *Crypto Intel Zone* — nosso grupo premium de analises e operacoes. 💎",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
 
    elif query.data == "mentoria":
        keyboard = [[InlineKeyboardButton("🎓 Falar com suporte", url=SUPORTE_LINK)]]
        await query.message.reply_text(
            "🎓 *Mentoria Wall Street Girls*\n\n"
            "Para quem quer acelerar resultados.\n\n"
            "📈 Acompanhamento próximo\n"
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
    texto    = update.message.text.strip()
 
    if user_id in aguardando_uid:
        aguardando_uid.discard(user_id)
        db = carregar_db()
        db[str(user_id)] = db.get(str(user_id), {})
        db[str(user_id)]["nome"]     = nome
        db[str(user_id)]["username"] = username
        db[str(user_id)]["ativo"]    = False
        db[str(user_id)]["via"]      = "Corretora (UID)"
        salvar_db(db)
 
        await enviar_para_suporte(context, user_id, nome, username, "Corretora (UID)", "UID: " + texto)
        await update.message.reply_text(
            "✅ *UID recebido!*\n\n"
            "Estamos verificando e vamos liberar seu acesso em breve. 🕐\n\n"
            "Qualquer duvida: @suportewsg",
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
        db[str(user_id)]["via"]      = "Infinitepay"
        salvar_db(db)
 
        await enviar_para_suporte(context, user_id, nome, username, "Infinitepay")
        await update.message.forward(chat_id=ADMIN_ID)
        await update.message.reply_text(
            "✅ *Comprovante recebido!*\n\n"
            "Estamos verificando e vamos liberar seu acesso em breve. 🕐\n\n"
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
        db[str(user_id)]["via"]      = "Infinitepay"
        salvar_db(db)
 
        await enviar_para_suporte(context, user_id, nome, username, "Infinitepay")
        await update.message.forward(chat_id=ADMIN_ID)
        await update.message.reply_text(
            "✅ *Comprovante recebido!*\n\n"
            "Estamos verificando e vamos liberar seu acesso em breve. 🕐\n\n"
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
