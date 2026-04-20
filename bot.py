from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes,
)
import os, json, datetime
 
# ── Configuração ───────────────────────────────────────────────────────────────
TOKEN        = os.getenv("TOKEN")
VIP_GROUP_ID = -1002336704499
ADMIN_ID     = 5908958242
 
# Produtos
HOTMART_INTEL = "https://pay.hotmart.com/M105464502I"
HOTMART_LT    = "https://pay.hotmart.com/M105464662R"
 
# Corretoras
LINK_MEXC   = "https://promote.mexc.com/a/z6V3qkQL"
LINK_BINGEX = "https://bingx.com/partner/wallstreetgirls"
 
# Calendly
CALENDLY_LINK = "https://calendly.com/wallstreet_girls"
 
# Equipe — quando tiver o @ da Sabrina, substitua COLOCAR_USERNAME_SABRINA
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
 
# Estados em memória
aguardando_comprovante = set()
aguardando_email: dict = {}
 
# ── Helpers ────────────────────────────────────────────────────────────────────
def _username(user) -> str:
    return f"@{user.username}" if user.username else "sem username"
 
def _get_sales_rotation(user_id: str) -> tuple:
    """Rotação: 1ª Sabrina → 2ª Carlo → 3ª+ Suporte."""
    db = carregar_db()
    count = db.get(user_id, {}).get("sales_contact_count", 0) + 1
    db.setdefault(user_id, {})["sales_contact_count"] = count
    salvar_db(db)
    if count == 1:
        return SABRINA_USERNAME, "Sabrina"
    elif count == 2:
        return CARLO_USERNAME, "Carlo"
    else:
        return SUPORTE_USERNAME, "Suporte"
 
def _notificar_lead(nome, username, user_id, email, atendente) -> str:
    return (
        f"✦ *Novo lead — Suporte de Vendas*\n\n"
        f"👤  {nome}\n"
        f"📎  {username}\n"
        f"🆔  `{user_id}`\n"
        f"✉️  {email}\n"
        f"→  Direcionado para *{atendente}*\n"
        f"🕐  {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )
 
# ── Menu principal ─────────────────────────────────────────────────────────────
def _menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("◆ Intel Zone — Análises & Ideias de Trade", callback_data="vip")],
        [InlineKeyboardButton("◆ Grupos Premium",                          callback_data="grupos")],
        [InlineKeyboardButton("◆ Corretoras Parceiras",                    callback_data="corretoras")],
        [InlineKeyboardButton("◇ Conteúdo Gratuito",                      callback_data="conteudo")],
        [InlineKeyboardButton("◇ Mentoria",                                callback_data="mentoria")],
        [InlineKeyboardButton("✦ Enviar Comprovante",                      callback_data="pagar_vip")],
        [InlineKeyboardButton("○ Suporte de Vendas",                       callback_data="suporte_vendas")],
        [InlineKeyboardButton("○ Suporte ao Cliente",                      url=SUPORTE_LINK)],
    ])
 
# ── /start ─────────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✦ *Wall Street Girls*\n\n"
        "Um ecossistema para quem opera com estratégia e consistência.\n"
        "Aqui você não depende de sorte — você aprende a ler o mercado.\n\n"
        "─────────────────────\n"
        "Escolha como quer começar:",
        parse_mode="Markdown",
        reply_markup=_menu_keyboard(),
    )
 
# ── Intel Zone (VIP legado) ────────────────────────────────────────────────────
async def cb_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✦ Assinar por R$79,90/mês", callback_data="pagar_vip")],
        [InlineKeyboardButton("← Voltar", callback_data="voltar")],
    ])
    await query.message.reply_text(
        "◆ *Intel Zone — Análises & Ideias de Trade*\n\n"
        "Você não recebe sinal de terceiro.\n"
        "Você acompanha *a análise acontecendo ao vivo.*\n\n"
        "Cada ideia justificada. Cada decisão explicada.\n"
        "Você evolui enquanto opera.\n\n"
        "─────────────────────\n"
        "✦ *O que está incluído:*\n\n"
        "  ◦ Análises técnicas diárias — cripto, petróleo, gás e metais\n"
        "  ◦ Ideias de trade com raciocínio completo\n"
        "  ◦ Comunidade exclusiva de traders\n\n"
        "─────────────────────\n"
        "  *R$79,90 / mês*\n\n"
        "🎁 *Bônus:* 7 dias grátis de acesso ao *Intel Zone LT* — operações ao vivo em tempo real.\n\n"
        "─────────────────────",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
 
# ── Grupos Premium ─────────────────────────────────────────────────────────────
async def cb_grupos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✦ Assinar Intel Premium — R$79,90", url=HOTMART_INTEL)],
        [InlineKeyboardButton("✦ Assinar Live Trading — R$149,90", url=HOTMART_LT)],
        [InlineKeyboardButton("← Voltar", callback_data="voltar")],
    ])
    await query.message.reply_text(
        "◆ *Grupos Premium*\n\n"
        "─────────────────────\n"
        "◆ *Crypto Zone Intel Premium*  —  R$79,90/mês\n\n"
        "Análises técnicas diárias de cripto, petróleo, gás natural e metais. "
        "Conteúdo preciso, sem ruído. Ideal para quem quer desenvolver leitura "
        "gráfica profissional e tomar decisões com mais clareza.\n\n"
        "─────────────────────\n"
        "◆ *Crypto Zone Live Trading*  —  R$149,90/mês\n\n"
        "Operações ao vivo — cada entrada e saída acompanhada em tempo real, "
        "com o raciocínio explicado em cada movimento. "
        "Para quem quer absorver a mentalidade de um trader profissional na prática.\n\n"
        "─────────────────────",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
 
# ── Corretoras Parceiras ───────────────────────────────────────────────────────
async def cb_corretoras(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("◆ MEXC",   callback_data="corretora_mexc")],
        [InlineKeyboardButton("◆ BingX",  callback_data="corretora_bingex")],
        [InlineKeyboardButton("← Voltar", callback_data="voltar")],
    ])
    await query.message.reply_text(
        "◆ *Corretoras Parceiras*\n\n"
        "Opere nas nossas corretoras parceiras e desbloqueie um benefício exclusivo.\n\n"
        "─────────────────────\n"
        "🎁 *Bônus exclusivo*\n\n"
        "Após criar sua conta pelo nosso link e operar por pelo menos *1 semana*, "
        "você ganha *20 minutos gratuitos* comigo para analisarmos um gráfico juntos — ao vivo.\n\n"
        "─────────────────────\n"
        "Escolha sua corretora:",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
 
async def cb_corretora_mexc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✦ Abrir conta na MEXC", url=LINK_MEXC)],
        [InlineKeyboardButton("🎁 Já operei 1 semana — quero minha sessão", callback_data="solicitar_calendly_mexc")],
        [InlineKeyboardButton("← Voltar", callback_data="corretoras")],
    ])
    await query.message.reply_text(
        "◆ *MEXC — Corretora Parceira*\n\n"
        "1 — Abra sua conta gratuita pelo link abaixo\n"
        "2 — Deposite e opere por pelo menos *1 semana*\n"
        "3 — Solicite sua sessão gratuita de *20 minutos*\n\n"
        "─────────────────────",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
 
async def cb_corretora_bingex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✦ Abrir conta na BingX", url=LINK_BINGEX)],
        [InlineKeyboardButton("🎁 Já operei 1 semana — quero minha sessão", callback_data="solicitar_calendly_bingex")],
        [InlineKeyboardButton("← Voltar", callback_data="corretoras")],
    ])
    await query.message.reply_text(
        "◆ *BingX — Corretora Parceira*\n\n"
        "1 — Abra sua conta gratuita pelo link abaixo\n"
        "2 — Deposite e opere por pelo menos *1 semana*\n"
        "3 — Solicite sua sessão gratuita de *20 minutos*\n\n"
        "─────────────────────",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
 
# ── Solicitação Calendly ───────────────────────────────────────────────────────
async def _solicitar_calendly(update: Update, context: ContextTypes.DEFAULT_TYPE, corretora: str):
    query = update.callback_query
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
            f"✦ *Solicitação de sessão — {corretora}*\n\n"
            f"👤  {user.full_name}\n"
            f"📎  {username}\n"
            f"🆔  `{user_id}`\n\n"
            f"Para liberar: `/liberar {user_id}`"
        ),
        parse_mode="Markdown",
    )
    await query.message.reply_text(
        "✦ *Solicitação recebida.*\n\n"
        "Vou verificar sua conta na corretora e em até *24 horas* "
        "você receberá o link para agendar sua sessão gratuita.\n\n"
        "Fique de olho nas mensagens do bot.",
        parse_mode="Markdown",
    )
 
async def cb_solicitar_calendly_mexc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _solicitar_calendly(update, context, "MEXC")
 
async def cb_solicitar_calendly_bingex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _solicitar_calendly(update, context, "BingX")
 
# ── /liberar (admin) ───────────────────────────────────────────────────────────
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
            f"✦ *Sua sessão gratuita foi liberada.*\n\n"
            f"Clique no link abaixo para agendar seus *20 minutos* comigo.\n"
            f"Vamos analisar um gráfico juntos, ao vivo.\n\n"
            f"→ {CALENDLY_LINK}"
        ),
        parse_mode="Markdown",
    )
    await update.message.reply_text(
        f"✅ Calendly enviado para {info.get('nome')} ({info.get('username')})."
    )
 
# ── Suporte de Vendas — captura email primeiro ─────────────────────────────────
async def cb_suporte_vendas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query   = update.callback_query
    await query.answer()
    user_id = query.from_user.id
 
    # Mostra destino sem incrementar ainda
    db    = carregar_db()
    count = db.get(str(user_id), {}).get("sales_contact_count", 0)
    if count == 0:
        destino_nome = "Sabrina"
    elif count == 1:
        destino_nome = "Carlo"
    else:
        destino_nome = "Suporte"
 
    aguardando_email[user_id] = destino_nome
 
    await query.message.reply_text(
        f"◆ *Suporte de Vendas*\n\n"
        f"Em instantes você será direcionado para *{destino_nome}*.\n\n"
        "Antes de continuar, informe seu *e-mail* para que possamos "
        "acompanhar melhor o seu atendimento:\n\n"
        "_Digite seu e-mail abaixo:_",
        parse_mode="Markdown",
    )
 
# ── Conteúdo gratuito ──────────────────────────────────────────────────────────
async def cb_conteudo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("▶ YouTube",   url=YOUTUBE_LINK)],
        [InlineKeyboardButton("◈ TikTok",    url=TIKTOK_LINK)],
        [InlineKeyboardButton("◉ Instagram", url=INSTAGRAM_LINK)],
        [InlineKeyboardButton("← Voltar",    callback_data="voltar")],
    ])
    await query.message.reply_text(
        "◇ *Conteúdo Gratuito*\n\n"
        "Acompanhe nossa visão de mercado, análises e estratégias:",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
 
# ── Mentoria ───────────────────────────────────────────────────────────────────
async def cb_mentoria(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("○ Falar com suporte", url=SUPORTE_LINK)],
        [InlineKeyboardButton("← Voltar", callback_data="voltar")],
    ])
    await query.message.reply_text(
        "◇ *Mentoria Wall Street Girls*\n\n"
        "Para quem quer acelerar resultados com acompanhamento próximo.\n\n"
        "  ◦ Desenvolvimento de mentalidade\n"
        "  ◦ Direcionamento estratégico\n"
        "  ◦ Acompanhamento individualizado\n\n"
        "─────────────────────\n"
        "Fale com o suporte para saber mais:",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
 
# ── Pagar VIP / enviar comprovante ────────────────────────────────────────────
async def cb_pagar_vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    aguardando_comprovante.add(query.from_user.id)
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✦ Assinar Intel Premium — R$79,90", url=HOTMART_INTEL)],
        [InlineKeyboardButton("✦ Assinar Live Trading — R$149,90", url=HOTMART_LT)],
    ])
    await query.message.reply_text(
        "✦ *Acesso aos Grupos Premium*\n\n"
        "1 — Escolha seu plano e efetue o pagamento\n"
        "2 — Volte aqui e envie o comprovante (foto ou texto)\n"
        "3 — Validamos e enviamos o link do grupo ✅\n\n"
        "─────────────────────\n"
        "⚠️ Após o pagamento, envie o comprovante aqui.\n\n"
        "Dúvidas: @suportewsg",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )
 
# ── Registrar e notificar acesso ───────────────────────────────────────────────
async def registrar_e_notificar(context, user_id, nome, username, via):
    link_obj = await context.bot.create_chat_invite_link(
        chat_id=VIP_GROUP_ID,
        member_limit=1,
        expire_date=datetime.datetime.now() + datetime.timedelta(hours=48),
    )
    link = link_obj.invite_link
 
    db = carregar_db()
    db[str(user_id)] = {
        "ativo":      True,
        "nome":       nome,
        "username":   username,
        "via":        via,
        "entrou_em":  datetime.datetime.now().isoformat(),
        "renovar_em": (datetime.datetime.now() + datetime.timedelta(days=30)).isoformat(),
    }
    salvar_db(db)
 
    await context.bot.send_message(
        chat_id=user_id,
        text=(
            "✦ *Acesso liberado!*\n\n"
            "Bem-vindo(a) ao *Intel Zone*.\n\n"
            "→ " + link + "\n\n"
            "⚠️ Link de uso único — expira em 48h. Não compartilhe.\n\n"
            "Qualquer dúvida: @suportewsg"
        ),
        parse_mode="Markdown",
    )
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"✦ *Novo membro — Intel Zone*\n\n"
            f"👤  {nome}\n"
            f"📎  {username}\n"
            f"🆔  {user_id}\n"
            f"📥  {via}\n"
            f"🕐  {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}"
        ),
    )
 
async def enviar_para_suporte_admin(context, user_id, nome, username, via, mensagem_extra=""):
    db = carregar_db()
    db.setdefault(str(user_id), {}).update({"nome": nome, "username": username, "ativo": False})
    salvar_db(db)
 
    keyboard = [[
        InlineKeyboardButton("✅ Liberar acesso", callback_data=f"liberar_{user_id}"),
        InlineKeyboardButton("✕ Recusar",         callback_data=f"recusar_{user_id}"),
    ]]
    texto = (
        f"◆ *Nova solicitação de acesso*\n\n"
        f"👤  {nome}\n"
        f"📎  {username}\n"
        f"🆔  {user_id}\n"
        f"📥  {via}\n"
    )
    if mensagem_extra:
        texto += f"📝  {mensagem_extra}\n"
    texto += "\n─────────────────────\n👇 Verifique e libere o acesso:"
 
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=texto,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
 
# ── Voltar ao menu ─────────────────────────────────────────────────────────────
async def cb_voltar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "Escolha como quer continuar:",
        reply_markup=_menu_keyboard(),
    )
 
# ── Callback genérico (liberar/recusar comprovante) ───────────────────────────
async def escolha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
 
    if query.data.startswith("liberar_"):
        target_id = int(query.data.split("_")[1])
        db        = carregar_db()
        dados     = db.get(str(target_id), {})
        try:
            await registrar_e_notificar(
                context, target_id,
                dados.get("nome", str(target_id)),
                dados.get("username", "-"),
                dados.get("via", "-"),
            )
            await query.message.reply_text(f"✅ Acesso liberado para {dados.get('nome', target_id)}.")
        except Exception as e:
            await query.message.reply_text(f"✕ Erro: {e}")
 
    elif query.data.startswith("recusar_"):
        target_id = int(query.data.split("_")[1])
        await context.bot.send_message(
            chat_id=target_id,
            text=(
                "✕ *Não foi possível validar seu acesso.*\n\n"
                "Possíveis motivos:\n"
                "  ◦ Comprovante não identificado\n"
                "  ◦ Pagamento não confirmado\n\n"
                "Fale com o suporte e resolvemos: @suportewsg"
            ),
            parse_mode="Markdown",
        )
        await query.message.reply_text("✕ Solicitação recusada.")
 
# ── Receber texto ──────────────────────────────────────────────────────────────
async def receber_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user     = update.message.from_user
    user_id  = user.id
    nome     = user.full_name
    username = _username(user)
 
    # Aguardando email para suporte de vendas
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
            [InlineKeyboardButton(f"◆ Falar com {atendente_nome}", url=f"https://t.me/{atendente_user}")],
        ])
        await update.message.reply_text(
            f"✦ *Tudo certo!*\n\n"
            f"*{atendente_nome}* está pronto(a) para te atender.\n\n"
            f"─────────────────────",
            parse_mode="Markdown",
            reply_markup=keyboard,
        )
        return
 
    # Aguardando comprovante
    if user_id in aguardando_comprovante:
        aguardando_comprovante.discard(user_id)
        db = carregar_db()
        db.setdefault(str(user_id), {}).update({
            "nome": nome, "username": username,
            "ativo": False, "via": "Hotmart",
        })
        salvar_db(db)
        await enviar_para_suporte_admin(context, user_id, nome, username, "Hotmart")
        await update.message.forward(chat_id=ADMIN_ID)
        await update.message.reply_text(
            "✦ *Comprovante recebido.*\n\n"
            "Estamos verificando e liberamos seu acesso em breve.\n\n"
            "Dúvidas: @suportewsg",
            parse_mode="Markdown",
        )
        return
 
    await update.message.reply_text(
        "Use o menu abaixo para navegar:",
        reply_markup=_menu_keyboard(),
    )
 
# ── Receber foto ───────────────────────────────────────────────────────────────
async def receber_foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user     = update.message.from_user
    user_id  = user.id
    nome     = user.full_name
    username = _username(user)
 
    if user_id in aguardando_comprovante:
        aguardando_comprovante.discard(user_id)
        db = carregar_db()
        db.setdefault(str(user_id), {}).update({
            "nome": nome, "username": username,
            "ativo": False, "via": "Hotmart",
        })
        salvar_db(db)
        await enviar_para_suporte_admin(context, user_id, nome, username, "Hotmart")
        await update.message.forward(chat_id=ADMIN_ID)
        await update.message.reply_text(
            "✦ *Comprovante recebido.*\n\n"
            "Estamos verificando e liberamos seu acesso em breve.\n\n"
            "Dúvidas: @suportewsg",
            parse_mode="Markdown",
        )
 
# ── /membros (admin) ───────────────────────────────────────────────────────────
async def listar_membros(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return
    db = carregar_db()
    if not db:
        await update.message.reply_text("Nenhum membro registrado.")
        return
    texto = "◆ *Membros registrados*\n\n"
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
 
# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    app = ApplicationBuilder().token(TOKEN).build()
 
    app.add_handler(CommandHandler("start",   start))
    app.add_handler(CommandHandler("membros", listar_membros))
    app.add_handler(CommandHandler("liberar", liberar_calendly))
 
    app.add_handler(CallbackQueryHandler(cb_vip,                       pattern="^vip$"))
    app.add_handler(CallbackQueryHandler(cb_grupos,                    pattern="^grupos$"))
    app.add_handler(CallbackQueryHandler(cb_corretoras,                pattern="^corretoras$"))
    app.add_handler(CallbackQueryHandler(cb_corretora_mexc,            pattern="^corretora_mexc$"))
    app.add_handler(CallbackQueryHandler(cb_corretora_bingex,          pattern="^corretora_bingex$"))
    app.add_handler(CallbackQueryHandler(cb_solicitar_calendly_mexc,   pattern="^solicitar_calendly_mexc$"))
    app.add_handler(CallbackQueryHandler(cb_solicitar_calendly_bingex, pattern="^solicitar_calendly_bingex$"))
    app.add_handler(CallbackQueryHandler(cb_suporte_vendas,            pattern="^suporte_vendas$"))
    app.add_handler(CallbackQueryHandler(cb_conteudo,                  pattern="^conteudo$"))
    app.add_handler(CallbackQueryHandler(cb_mentoria,                  pattern="^mentoria$"))
    app.add_handler(CallbackQueryHandler(cb_pagar_vip,                 pattern="^pagar_vip$"))
    app.add_handler(CallbackQueryHandler(cb_voltar,                    pattern="^voltar$"))
    app.add_handler(CallbackQueryHandler(escolha))
 
    app.add_handler(MessageHandler(filters.PHOTO,                      receber_foto))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,    receber_texto))
 
    app.run_polling()
 
if __name__ == "__main__":
    main()
