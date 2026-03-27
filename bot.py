from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "7804710764:AAFIb3LhhJl77WogfPfs9BbcxVfHsQqkStw"
ADMIN_ID = 6834599479

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("1️⃣ Register", callback_data="register")],
        [InlineKeyboardButton("2️⃣ Send UID", callback_data="uid")],
        [InlineKeyboardButton("3️⃣ Deposit Screenshot", callback_data="deposit")],
        [InlineKeyboardButton("4️⃣ Admin Approval", callback_data="admin")]
    ]
    await update.message.reply_text(
        "🔥 Welcome to BDG WITH VERHAM 🔥\n\nSelect Option 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# BUTTON CLICK
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "register":
        await query.edit_message_text(
            "✅ Register Here 👇\nhttps://bdg-ipl.shop//#/register?invitationCode=6437315916837"
        )

    elif query.data == "uid":
        context.user_data["step"] = "uid"
        await query.edit_message_text("📩 Apna UID bhejo")

    elif query.data == "deposit":
        context.user_data["step"] = "deposit"
        await query.edit_message_text("💰 Screenshot bhejo")

    elif query.data == "admin":
        await query.edit_message_text("⏳ Approval ka wait karo")

# USER MESSAGE HANDLE
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if context.user_data.get("step") == "uid":
        uid = update.message.text
        await update.message.reply_text("✅ UID submit ho gaya")

        keyboard = [[
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
        ]]

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 UID Request\nUser: {user.first_name}\nID: {user.id}\nUID: {uid}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif context.user_data.get("step") == "deposit":
        if update.message.photo:
            await update.message.reply_text("✅ Screenshot submit ho gaya")

            keyboard = [[
                InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
            ]]

            await context.bot.forward_message(
                chat_id=ADMIN_ID,
                from_chat_id=update.message.chat_id,
                message_id=update.message.message_id
            )

            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"📸 Screenshot from {user.first_name} (ID: {user.id})",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

# ADMIN ACTION
async def admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("approve_"):
        user_id = int(data.split("_")[1])
        await context.bot.send_message(chat_id=user_id, text="✅ Approved! Aapka request accept ho gaya 🎉")
        await query.edit_message_text("✅ Approved")

    elif data.startswith("reject_"):
        user_id = int(data.split("_")[1])
        await context.bot.send_message(chat_id=user_id, text="❌ Rejected! Please try again.")
        await query.edit_message_text("❌ Rejected")

# RUN
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_click, pattern="^(register|uid|deposit|admin)$"))
app.add_handler(CallbackQueryHandler(admin_action, pattern="^(approve_|reject_)"))
app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_message))

app.run_polling()
