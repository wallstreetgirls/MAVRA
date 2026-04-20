"""
Wall Street Girls — Bot Telegram
Requer: python-telegram-bot>=20.0, flask
 
Variáveis de ambiente no Railway:
  TOKEN            → token do bot (@BotFather)
  WEBHOOK_SECRET   → string secreta que você cadastra no Hotmart (ex: wsg2026)
  PORT             → Railway define automaticamente (não precisa setar)
"""
 
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes,
)
from flask import Flask, request as flask_request
import os, json, datetime, threading, asyncio
 
# ── Configuração ───────────────────────────────────────────────────────────────
TOKEN          = os.getenv("TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "wsg2026")
PORT           = int(os.getenv("PORT", 8080))
 
INTEL_GROUP_ID      = -1002336704499  # CZ Intel Premium
LIVE_TRADING_GROUP_ID = -5120143530   # CZ Live Trading
ADMIN_ID            = 5908958242
 
# Produtos
HOTMART_INTEL = "https://pay.hotmart.com/M105464502I"
HOTMART_LT    = "https://pay.hotmart.com/M105464662R"
 
# Corretoras
LINK_MEXC   = "https://promote.mexc.com/a/z6V3qkQL"
LINK_BINGEX = "https://bingx.com/partner/wallstreetgirls"
 
# Calendly
CALENDLY_LINK = "https://calendly.com/wallstreet_girls"
 
# Equipe
SABRINA_USERNAME = os.getenv("SABRINA_USERNAME", "COLOCAR_USERNAME_SABRINA")
CARLO_USERNAME   = "carlodeluca"
SUPORTE_USERNAME = "suportewsg"
 
# Redes sociais
SUPORTE_LINK   = "https://t.me/suportewsg"
YOUTUBE_LINK   = "https://youtube.com/@wallstreet_girls"
TIKTOK_LINK    = "https://tiktok.com/@wallstreet.girls"
INSTAGRAM_LINK = "https://instagram.com/wallstreet_girls"
 
# ── Persistência ───────────────────────────────────────────────────────────────
DB_FILE = "assinantes.json"
 
def carregar_db() -> dict:
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)
 
def salvar_db(db: dict):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)
 
aguardando_email: dict = {}
 
# ── Helpers ────────────────────────────────────────────────────────────────────
def _username(user) -> str:
    return f"@{user.username}" if user.username else "sem username"
 
def _get_sales_rotation(user_id: str) -> tuple:
    db = carregar_db()
    count = db.get(user_id, {}).get("sales_contact_count", 0) + 1
    db.setdefault(user_id, {})["sales_contact_count"] = count
    salvar_db(db)
    if count % 2 == 1:
        return SABRINA_USERNAME, "Sabrina"
    else:
        return CARLO_USERNAME, "Carlo"
 
def _notificar_lead(nome, username, user_id, email, atendente) -> str:
    return (
        f"🔔 *Novo lead — Suporte de Vendas*\n\n"
        f"👤  {nome}\n"
        f"📎  {username}\n"
        f"🆔  `{user_id}`\n"
        f"✉️  {email}\n"
        f"➡️  Direcionado para *{atendente}*\n"
        f"🕐  {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )
 
# ── Menu principal ─────────────────────────────────────────────────────────────
def _menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔴 CZ // Live Trading — Operações ao Vivo", callback_data="produto_lt")],
        [InlineKeyboardButton("📊 CZ Intel Premium — Análises & Ideias",   callback_data="produto_intel")],
        [InlineKeyboardButton("💬 Suporte de Vendas",                      callback_data="suporte_vendas")],
        [InlineKeyboardButton("📱 Conteúdo Gratuito",                      callback_data="conteudo")],
        [InlineKeyboardButton("📅 1:1 com a Mava — Grátis",               callback_data="um_a_um")],
        [InlineKeyboardButton("🛟 SAC — Atendimento ao Cliente",           url=SUPORTE_LINK)],
    ])
 
# ── /start ─────────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Só responde no privado
    if update.effective_chat.type != "private":
        return
 
    await update.message.reply_text(
        "✦ *Wall Street Girls*\n\n"
        "Um ecossistema para quem opera com estratégia e consistência.\n"
        "Aqui você não depende de sorte — você aprende a ler o mercado.\n\n"
        "Qualquer dúvida, fale com @suportewsg.\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "👇 Escolha como quer começar:",
        parse_mode="Markdown",
        reply_markup=_menu_keyboard(),
    )
 
# ── CZ Live Trading ────────────────────────────────────────────────────────────
async def cb_produto_lt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Acessar página de vendas", url=HOTMART_LT)],
        [InlineKeyboardButton("← Voltar", callback_data="voltar")],
    ])
    await query.message.reply_text(
        "🔴 *CZ // Live Trading — Operações ao Vivo*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Você acompanha *cada operação acontecendo em tempo real.*\n\n"
        "Não é sinal. Não é resumo.\n"
        "É o trader operando ao vivo — entrada, saída, raciocínio.\n"
        "Você aprende vendo, não lendo.\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "✅  Operações ao vivo no Telegram\n"
        "✅  Raciocínio explicado em cada movimento\n"
        "✅  Cripto, petróleo, gás natural e metais\n"
        "✅  Acesso imediato após assinatura\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💰  *R$149,90 / mês*\n\n"
        "👇 Clique abaixo para acessar a página de vendas:",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
 
# ── CZ Intel Premium ───────────────────────────────────────────────────────────
async def cb_produto_intel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Acessar página de vendas", url=HOTMART_INTEL)],
        [InlineKeyboardButton("← Voltar", callback_data="voltar")],
    ])
    await query.message.reply_text(
        "📊 *CZ Intel Premium — Análises & Ideias de Trade*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Você não recebe sinal de terceiro.\n"
        "Você acompanha *a análise sendo construída*, com cada decisão justificada.\n\n"
        "Ideal para quem quer desenvolver leitura gráfica real\n"
        "e operar com mais clareza e consistência.\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "✅  Análises técnicas diárias\n"
        "✅  Ideias de trade com raciocínio completo\n"
        "✅  Cripto, petróleo, gás natural e metais\n"
        "✅  Comunidade exclusiva de traders\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💰  *R$79,90 / mês*\n\n"
        "👇 Clique abaixo para acessar a página de vendas:",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
 
# ── 1:1 com a Mava ────────────────────────────────────────────────────────────
async def cb_um_a_um(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📅 Agendar minha sessão grátis", url=CALENDLY_LINK)],
        [InlineKeyboardButton("🏦 Ver corretoras parceiras", callback_data="ver_corretoras")],
        [InlineKeyboardButton("← Voltar", callback_data="voltar")],
    ])
    await query.message.reply_text(
        "📅 *1:1 com a Mava — Grátis*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Quer dar o primeiro passo no mercado financeiro com o pé direito?\n\n"
        "Em *20 minutos* eu te mostro:\n\n"
        "  📊  Como analisar um gráfico na prática\n"
        "  🏦  Qual corretora faz mais sentido pro seu perfil\n"
        "  🎯  Por onde começar sem queimar dinheiro\n\n"
        "*Gratuito. Sem compromisso.*\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🏦 *Como ganhar essa sessão?*\n\n"
        "Simples — abra sua conta em uma das nossas corretoras parceiras "
        "pelo nosso link e opere por *1 semana*.\n"
        "Depois é só solicitar e a sessão é sua. ✅\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "👇 Agende agora ou veja as corretoras:",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
 
async def cb_ver_corretoras(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🟡 Abrir conta na MEXC",  callback_data="corretora_mexc")],
        [InlineKeyboardButton("🔵 Abrir conta na BingX", callback_data="corretora_bingex")],
        [InlineKeyboardButton("← Voltar", callback_data="um_a_um")],
    ])
    await query.message.reply_text(
        "🏦 *Corretoras Parceiras*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Escolha sua corretora, abra a conta pelo nosso link e\n"
        "opere por *1 semana* para desbloquear a sessão gratuita:",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
 
async def cb_corretora_mexc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🟡 Criar conta na MEXC", url=LINK_MEXC)],
        [InlineKeyboardButton("🎁 Já operei 1 semana — quero minha sessão!", callback_data="solicitar_calendly_mexc")],
        [InlineKeyboardButton("← Voltar", callback_data="ver_corretoras")],
    ])
    await query.message.reply_text(
        "🟡 *MEXC — Corretora Parceira*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "1️⃣  Crie sua conta gratuita pelo link abaixo\n"
        "2️⃣  Deposite e opere por pelo menos *1 semana*\n"
        "3️⃣  Clique em *Já operei* para solicitar sua sessão\n\n"
        "━━━━━━━━━━━━━━━━━━━━",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
 
async def cb_corretora_bingex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔵 Criar conta na BingX", url=LINK_BINGEX)],
        [InlineKeyboardButton("🎁 Já operei 1 semana — quero minha sessão!", callback_data="solicitar_calendly_bingex")],
        [InlineKeyboardButton("← Voltar", callback_data="ver_corretoras")],
    ])
    await query.message.reply_text(
        "🔵 *BingX — Corretora Parceira*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "1️⃣  Crie sua conta gratuita pelo link abaixo\n"
        "2️⃣  Deposite e opere por pelo menos *1 semana*\n"
        "3️⃣  Clique em *Já operei* para solicitar sua sessão\n\n"
        "━━━━━━━━━━━━━━━━━━━━",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
 
# ── Solicitação Calendly ───────────────────────────────────────────────────────
async def _solicitar_calendly(update: Update, context: ContextTypes.DEFAULT_TYPE, corretora: str):
    query    = update.callback_query
    await query.answer()
    user     = query.from_user
    user_id  = str(user.id)
    username = _username(user)
 
    db = carregar_db()
    db.setdefault(user_id, {})["calendly_pending"] = {
        "corretora": corretora,
        "username":  username,
        "nome":      user.full_name,
    }
    salvar_db(db)
 
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"🔔 *Solicitação de sessão — {corretora}*\n\n"
            f"👤  {user.full_name}\n"
            f"📎  {username}\n"
            f"🆔  `{user_id}`\n\n"
            f"Para liberar: `/liberar {user_id}`"
        ),
        parse_mode="Markdown",
    )
    await query.message.reply_text(
        "✅ *Solicitação recebida!*\n\n"
        "Vou verificar sua conta na corretora e em até *24 horas* "
        "você receberá o link para agendar sua sessão.\n\n"
        "Fique de olho nas mensagens do bot. 👀",
        parse_mode="Markdown",
    )
 
async def cb_solicitar_calendly_mexc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _solicitar_calendly(update, context, "MEXC")
 
async def cb_solicitar_calendly_bingex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _solicitar_calendly(update, context, "BingX")
 
# ── /liberar Calendly (admin) ──────────────────────────────────────────────────
async def liberar_calendly(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("Uso: `/liberar <user_id>`", parse_mode="Markdown")
        return
 
    target_id = context.args[0]
    db        = carregar_db()
    info      = db.get(target_id, {}).get("calendly_pending")
 
    if not info:
        await update.message.reply_text(f"⚠️ Nenhuma solicitação pendente para `{target_id}`.", parse_mode="Markdown")
        return
 
    del db[target_id]["calendly_pending"]
    salvar_db(db)
 
    await context.bot.send_message(
        chat_id=int(target_id),
        text=(
            f"🎉 *Sua sessão foi liberada!*\n\n"
            f"Clique no link abaixo para agendar seus *20 minutos* comigo.\n\n"
            f"📅  {CALENDLY_LINK}"
        ),
        parse_mode="Markdown",
    )
    await update.message.reply_text(
        f"✅ Calendly enviado para {info.get('nome')} ({info.get('username')})."
    )
 
# ── Suporte de Vendas ──────────────────────────────────────────────────────────
async def cb_suporte_vendas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    await query.answer()
    user_id = query.from_user.id
 
    db    = carregar_db()
    count = db.get(str(user_id), {}).get("sales_contact_count", 0)
    destino_nome = "Sabrina" if count % 2 == 0 else "Carlo"
 
    aguardando_email[user_id] = destino_nome
 
    await query.message.reply_text(
        f"💬 *Suporte de Vendas*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Em instantes você será direcionado para *{destino_nome}*.\n\n"
        f"Para agilizar seu atendimento, informe seu *e-mail*:\n\n"
        f"_Digite seu e-mail abaixo 👇_",
        parse_mode="Markdown",
    )
 
# ── Conteúdo gratuito ──────────────────────────────────────────────────────────
async def cb_conteudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("▶️ YouTube",   url=YOUTUBE_LINK)],
        [InlineKeyboardButton("🎵 TikTok",    url=TIKTOK_LINK)],
        [InlineKeyboardButton("📸 Instagram", url=INSTAGRAM_LINK)],
        [InlineKeyboardButton("← Voltar",     callback_data="voltar")],
    ])
    await query.message.reply_text(
        "📱 *Conteúdo Gratuito*\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Acompanhe análises, estratégias e visão de mercado:",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
 
# ── Voltar ao menu ─────────────────────────────────────────────────────────────
async def cb_voltar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "👇 Escolha como quer continuar:",
        reply_markup=_menu_keyboard(),
    )
 
# ── Receber texto (APENAS NO PRIVADO) ─────────────────────────────────────────
async def receber_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Ignora qualquer mensagem que não seja conversa privada com o bot
    if update.effective_chat.type != "private":
        return
 
    user     = update.message.from_user
    user_id  = user.id
    nome     = user.full_name
    username = _username(user)
 
    if user_id in aguardando_email:
        email   = update.message.text.strip()
        aguardando_email.pop(user_id)
 
        atendente_user, atendente_nome = _get_sales_rotation(str(user_id))
 
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=_notificar_lead(nome, username, user_id, email, atendente_nome),
            parse_mode="Markdown",
        )
 
        db = carregar_db()
        db.setdefault(str(user_id), {})["email"] = email
        salvar_db(db)
 
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"💬 Falar com {atendente_nome}", url=f"https://t.me/{atendente_user}")],
        ])
        await update.message.reply_text(
            f"✅ *Tudo certo!*\n\n"
            f"*{atendente_nome}* está pronto(a) para te atender agora.\n\n"
            f"━━━━━━━━━━━━━━━━━━━━",
            parse_mode="Markdown",
            reply_markup=keyboard,
        )
        return
 
    await update.message.reply_text(
        "👇 Use o menu abaixo para navegar:",
        reply_markup=_menu_keyboard(),
    )
 
# ── /membros (admin) ───────────────────────────────────────────────────────────
async def listar_membros(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return
    db = carregar_db()
    if not db:
        await update.message.reply_text("Nenhum membro registrado.")
        return
    texto = "📋 *Membros registrados*\n\n"
    for i, (uid, d) in enumerate(db.items(), 1):
        status = "✅ Ativo" if d.get("ativo") else "⏳ Pendente"
        texto += (
            f"{i}. *{d.get('nome', '-')}* — {d.get('username', '-')}\n"
            f"   🆔 {uid}  |  {status}\n"
            f"   ✉️ {d.get('email', '-')}  |  📥 {d.get('via', '-')}\n\n"
        )
        if len(texto) > 3500:
            await update.message.reply_text(texto, parse_mode="Markdown")
            texto = ""
    if texto:
        await update.message.reply_text(texto, parse_mode="Markdown")
 
# ══════════════════════════════════════════════════════════════════════════════
# WEBHOOK HOTMART
# ══════════════════════════════════════════════════════════════════════════════
flask_app = Flask(__name__)
bot_app   = None
 
@flask_app.route("/hotmart-webhook", methods=["POST"])
def hotmart_webhook():
    token = flask_request.headers.get("X-Hotmart-Hottok", "")
    if token != WEBHOOK_SECRET:
        return {"error": "unauthorized"}, 401
 
    data  = flask_request.json or {}
    event = data.get("event", "")
 
    buyer   = data.get("data", {}).get("buyer", {})
    nome    = buyer.get("name", "Desconhecido")
    email   = buyer.get("email", "-")
    produto = data.get("data", {}).get("product", {}).get("name", "-")
 
    if event == "PURCHASE_APPROVED":
        asyncio.run_coroutine_threadsafe(
            _hotmart_aprovado(nome, email, produto),
            bot_app.loop,
        )
    elif event == "PURCHASE_CANCELED":
        asyncio.run_coroutine_threadsafe(
            _hotmart_cancelado(nome, email, produto),
            bot_app.loop,
        )
 
    return {"ok": True}, 200
 
async def _hotmart_aprovado(nome: str, email: str, produto: str):
    db = carregar_db()
 
    telegram_id = None
    for uid, dados in db.items():
        if dados.get("email") == email:
            telegram_id = int(uid)
            break
 
    chave = str(telegram_id) if telegram_id else f"email_{email}"
    db[chave] = db.get(chave, {})
    db[chave].update({
        "ativo":      True,
        "nome":       nome,
        "email":      email,
        "via":        f"Hotmart — {produto}",
        "entrou_em":  datetime.datetime.now().isoformat(),
        "renovar_em": (datetime.datetime.now() + datetime.timedelta(days=30)).isoformat(),
    })
    salvar_db(db)
 
    if telegram_id:
        try:
            # Determina quais grupos liberar baseado no produto
            eh_live_trading = "live" in produto.lower() or "trading" in produto.lower()
 
            # Grupos a liberar
            grupos = [INTEL_GROUP_ID]
            if eh_live_trading:
                grupos.append(LIVE_TRADING_GROUP_ID)
 
            links = []
            for group_id in grupos:
                link_obj = await bot_app.bot.create_chat_invite_link(
                    chat_id=group_id,
                    member_limit=1,
                    expire_date=datetime.datetime.now() + datetime.timedelta(hours=48),
                )
                links.append(link_obj.invite_link)
 
            # Monta mensagem com os links
            if len(links) == 1:
                corpo_links = f"👇 Clique no link abaixo para entrar no grupo:\n{links[0]}"
            else:
                corpo_links = (
                    f"👇 Clique nos links abaixo para entrar nos grupos:\n\n"
                    f"📊 *CZ Intel Premium:*\n{links[0]}\n\n"
                    f"🔴 *CZ Live Trading:*\n{links[1]}"
                )
 
            await bot_app.bot.send_message(
                chat_id=telegram_id,
                text=(
                    "🎉 *Pagamento confirmado! Acesso liberado.*\n\n"
                    f"Bem-vindo(a) ao *{produto}*!\n\n"
                    + corpo_links + "\n\n"
                    "⚠️  Links de uso único — expiram em 48h. Não compartilhe.\n\n"
                    "Qualquer dúvida: @suportewsg"
                ),
                parse_mode="Markdown",
            )
            db[chave]["link_enviado"] = True
            salvar_db(db)
            aviso_admin = f"✅ Link(s) enviado(s) automaticamente para {nome}."
        except Exception as e:
            aviso_admin = f"⚠️ Não foi possível enviar link automático: {e}\nLibere manualmente."
    else:
        aviso_admin = (
            "⚠️ *Telegram ID não encontrado.*\n"
            "A pessoa ainda não interagiu com o bot.\n"
            "Localize pelo email e libere manualmente."
        )
 
    await bot_app.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"🟢 *Nova compra aprovada — Hotmart*\n\n"
            f"👤  {nome}\n"
            f"✉️  {email}\n"
            f"📦  {produto}\n"
            f"🕐  {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
            f"{aviso_admin}"
        ),
        parse_mode="Markdown",
    )
 
async def _hotmart_cancelado(nome: str, email: str, produto: str):
    await bot_app.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"🔴 *Cancelamento — Hotmart*\n\n"
            f"👤  {nome}\n"
            f"✉️  {email}\n"
            f"📦  {produto}\n"
            f"🕐  {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
            f"Verifique e remova o acesso do grupo manualmente."
        ),
        parse_mode="Markdown",
    )
 
# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    global bot_app
 
    bot_app = ApplicationBuilder().token(TOKEN).build()
 
    bot_app.add_handler(CommandHandler("start",   start))
    bot_app.add_handler(CommandHandler("membros", listar_membros))
    bot_app.add_handler(CommandHandler("liberar", liberar_calendly))
 
    bot_app.add_handler(CallbackQueryHandler(cb_produto_lt,                pattern="^produto_lt$"))
    bot_app.add_handler(CallbackQueryHandler(cb_produto_intel,             pattern="^produto_intel$"))
    bot_app.add_handler(CallbackQueryHandler(cb_suporte_vendas,            pattern="^suporte_vendas$"))
    bot_app.add_handler(CallbackQueryHandler(cb_conteudo,                  pattern="^conteudo$"))
    bot_app.add_handler(CallbackQueryHandler(cb_um_a_um,                   pattern="^um_a_um$"))
    bot_app.add_handler(CallbackQueryHandler(cb_ver_corretoras,            pattern="^ver_corretoras$"))
    bot_app.add_handler(CallbackQueryHandler(cb_corretora_mexc,            pattern="^corretora_mexc$"))
    bot_app.add_handler(CallbackQueryHandler(cb_corretora_bingex,          pattern="^corretora_bingex$"))
    bot_app.add_handler(CallbackQueryHandler(cb_solicitar_calendly_mexc,   pattern="^solicitar_calendly_mexc$"))
    bot_app.add_handler(CallbackQueryHandler(cb_solicitar_calendly_bingex, pattern="^solicitar_calendly_bingex$"))
    bot_app.add_handler(CallbackQueryHandler(cb_voltar,                    pattern="^voltar$"))
 
    # CORREÇÃO PRINCIPAL: filters.ChatType.PRIVATE garante que o bot
    # só responde a mensagens de texto no chat privado, nunca no grupo
    bot_app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE,
        receber_texto
    ))
 
    threading.Thread(
        target=lambda: flask_app.run(host="0.0.0.0", port=PORT),
        daemon=True,
    ).start()
 
    bot_app.run_polling()
 
if __name__ == "__main__":
    main()
