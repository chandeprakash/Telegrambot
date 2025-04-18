from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes, CallbackQueryHandler

# Define states
PHONE, AREA, DOCUMENTS = range(3)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Register Now", url="https://tinyurl.com/Delf0")],
        [InlineKeyboardButton("✔️ Done", callback_data="done")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "<b>🚀 Welcome to Delfo Rider Registration! 🏍️</b>\n\n"
        "📋 Before proceeding, please complete the registration form.\n\n"
        "After filling out the form, click the '✔️ Done' button below to complete your registration.",
        reply_markup=reply_markup,
        parse_mode="HTML"
    )
    return PHONE

# Ask for phone number
async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📞 Please send your phone number.",
                                    reply_markup=InlineKeyboardMarkup([
                                        [InlineKeyboardButton("📱 Send Phone Number", request_contact=True)]
                                    ]))
    return AREA

# Ask for delivery area
async def ask_area(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_phone = update.message.contact.phone_number
    context.user_data['phone'] = user_phone
    await update.message.reply_text("📍 Enter your preferred delivery area.")
    return DOCUMENTS

# Ask for documents
async def ask_documents(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['area'] = update.message.text
    await update.message.reply_text("📜 Upload your Driving License & ID Proof.")
    return ConversationHandler.END

# Show Rider Dashboard
async def show_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔹 Login 🚚", callback_data="login"), InlineKeyboardButton("🔹 Logout 🚚", callback_data="logout")],
        [InlineKeyboardButton("🔹 View Available Deliveries 📦", callback_data="available_deliveries")],
        [InlineKeyboardButton("🔹 My Deliveries 🚚", callback_data="my_deliveries")],
        [InlineKeyboardButton("🔹 Wallet 💰", callback_data="wallet")],
        [InlineKeyboardButton("🔹 Support 🆘", callback_data="support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🚴‍♂️ <b>Step 2: Rider Dashboard</b>\n\n"
        "📌 Your Digital ID: <b>RIDER-3001</b>\n"
        "🚴‍♂️ Total Deliveries: <b>50</b>\n"
        "💰 Earnings: <b>₹7,200</b>\n\n"
        "Choose an option below:",
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

# Show available deliveries
async def show_available_deliveries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Accept Order", callback_data="accept_order"), InlineKeyboardButton("❌ Reject Order", callback_data="reject_order")],
        [InlineKeyboardButton("📢 Orders History!", callback_data="order_history")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(
        "📌 <b>Your Digital ID: RIDER-3001</b>\n\n"
        "📦 <b>New Order Assigned!</b>\n"
        "📍 Pickup: <b>Pizza Palace</b> (<a href='MAP_LINK'>MAP</a>)\n"
        "📍 Delivery To: <b>Customer Address</b> (<a href='MAP_LINK'>MAP</a>)\n",
        reply_markup=reply_markup,
        parse_mode="HTML",
        disable_web_page_preview=True
    )

# Show order history
async def show_order_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text(
        "📜 <b>Your Order History</b>\n\n"
        "🆔 Order ID: 12345 - ✅ Delivered\n"
        "🆔 Order ID: 67890 - ❌ Cancelled\n",
        parse_mode="HTML"
    )

# Handle 'Done' button
async def complete_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "✅ Registration Verified! 🎉\n\n"
        "💳 Your Telegram Digital ID: <b>RIDER-3001</b>\n"
        "📌 Save this ID for support & verification.\n\n"
        "🚀 You can now start receiving delivery requests. Stay active and earn more! 🏍️💰",
        parse_mode="HTML"
    )
    await show_dashboard(query, context)

# Cancel function
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Registration cancelled.")
    return ConversationHandler.END

# Main function
def main():
    app = Application.builder().token("8104210950:AAFeVdHD8HZxMO11sSOwJqBlfnPO9v3dzIQ").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
            AREA: [MessageHandler(filters.CONTACT, ask_area)],
            DOCUMENTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_documents)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(conv_handler)
    app.add_handler(CallbackQueryHandler(complete_registration, pattern="^done$"))
    app.add_handler(CallbackQueryHandler(show_available_deliveries, pattern="^available_deliveries$"))
    app.add_handler(CallbackQueryHandler(show_order_history, pattern="^order_history$"))
    
    app.run_polling()

if __name__ == '__main__':
    main()