import bot
import db


if not db.get_all_words():
    db.add_rus_words()
    db.add_eng_words()


print("Starting bot...")
bot.bot.polling(none_stop=True)
