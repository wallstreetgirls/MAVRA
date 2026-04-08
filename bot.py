from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "SEU_TOKEN_AQUI"


# ✅ Função segura (NÃO VAI MAIS QUEBRAR)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if not user:
        return

    user_id = user.id
    nome = user.first_name

    await update.message.reply_text(
        f"Fala {nome}!\n\nSeu ID é: {user_id}\n\nBot funcionando 🚀"
    )


# ✅ Exemplo de validação (pra depois usar com pagamento)
async def validar_uid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if not user:
        return

    user_id = user.id

    await update.message.reply_text(
        f"UID validado com sucesso:\n{user_id}"
    )


# ✅ Handler de erro (evita crash)
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Erro detectado: {context.error}")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("validar", validar_uid))

    # handler de erro
    app.add_error_handler(error_handler)

    print("Bot rodando...")

    app.run_polling()


if __name__ == "__main__":
    main()
