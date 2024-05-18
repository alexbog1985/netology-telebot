import bot
import db


if not db.get_all_words():
    db.add_default_words()


print("Starting bot...")
bot.bot.infinity_polling(timeout=10, long_polling_timeout=5)
