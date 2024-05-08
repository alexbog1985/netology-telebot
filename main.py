import bot
import db


if not db.get_all_words():
    db.add_rus_words()
    db.add_eng_words()


print("Starting bot...")
bot.bot.infinity_polling(timeout=10, long_polling_timeout=5)
