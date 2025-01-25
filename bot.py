from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Ваш токен
BOT_TOKEN = 'my token'

# Переменная для хранения приветственного сообщения
welcome_text = "Привет! Спасибо, что добавили меня в группу! 😊"

# Функция для отправки приветственного сообщения
async def welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверяем, что бота добавили в группу
    if update.message.new_chat_members:
        for user in update.message.new_chat_members:
            if user.id == context.bot.id:  # Проверяем, что добавили именно нашего бота
                await update.message.reply_text(welcome_text)
            else:
                # Приветствуем нового участника
                await update.message.reply_text(f"Добро пожаловать, {user.first_name}! {welcome_text}")

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Создаём клавиатуру с кнопками
    keyboard = [
        ["Задать приветственное сообщение"],
        ["Пригласить в группу"],
        ["Помощь"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=reply_markup
    )

# Функция для обработки текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Задать приветственное сообщение":
        await update.message.reply_text("Введите новое приветственное сообщение:")
        context.user_data["awaiting_welcome_text"] = True  # Указываем, что ожидаем текст

    elif text == "Пригласить в группу":
        await update.message.reply_text(
            "Чтобы добавить меня в группу, выполните следующие шаги:\n\n"
            "1. Перейдите в группу, куда хотите добавить бота.\n"
            "2. Нажмите на название группы → 'Добавить участников'.\n"
            "3. Введите мой username: @ВашБот.\n"
            "4. Добавьте меня в группу.\n\n"
            "После этого я начну приветствовать новых участников!"
        )

    elif text == "Помощь":
        await update.message.reply_text(
            "Я бот, который может:\n"
            "1. Отправлять приветственное сообщение при добавлении в группу.\n"
            "2. Помочь вам добавить меня в группу.\n\n"
            "Используйте кнопки ниже для взаимодействия."
        )

    elif context.user_data.get("awaiting_welcome_text"):
        # Сохраняем новое приветственное сообщение
        global welcome_text
        welcome_text = text
        context.user_data["awaiting_welcome_text"] = False  # Сбрасываем флаг
        await update.message.reply_text(f"Приветственное сообщение обновлено:\n{welcome_text}")

    else:
        await update.message.reply_text("Используйте кнопки для взаимодействия.")

# Основная функция
def main():
    # Создаём приложение бота
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))  # Обработчик команды /start
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_message))  # Обработчик добавления в группу
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  # Обработчик текстовых сообщений

    # Запускаем бота
    print("Бот запущен...")
    application.run_polling()

# Запуск программы
if __name__ == "__main__":
    main()
