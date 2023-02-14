import os
from pathlib import Path
from telebot import TeleBot, types
from config import Config
import json
import validators

parent_dir = Path(os.path.abspath(__file__)).parent.parent.absolute()
config = Config.load_config(parent_dir.joinpath("config.ini"))
bot = TeleBot(config.telegram.bot_token)


@bot.message_handler(commands=["start"])
def start(msg):
    chat_id = msg.chat.id
    data = {}
    with open(parent_dir.joinpath("data.json"), "r") as f:
        try:
            data = json.load(f)
        except:
            print("Invalid data.json file, recreating")
        data["chat_id"] = chat_id

    with open(parent_dir.joinpath("data.json"), "w") as f:
        json.dump(data, f)

    bot.send_message(chat_id, "✅ Бот запущен, уведомления настроены")


@bot.message_handler(commands=["addquery"])
def add_query(msg):
    if msg.text.split()[1:] == []:
        bot.send_message(msg.chat.id, "⛔ Нужно написать URL!")
        return

    url = msg.text.split()[1:][0]
    if not validators.url(url):
        bot.send_message(msg.chat.id, "⛔ Невалидный URL")
        return

    data = {"queries": []}
    with open(parent_dir.joinpath("data.json"), "r") as f:
        try:
            data = json.load(f)
        except:
            print("Invalid data.json file, recreating")
        if data.get("queries") and type(data["queries"]) == list:
            if url in data["queries"]:
                bot.send_message(msg.chat.id, "⛔ Данный URL уже есть в списке")
                return
            else:
                data["queries"].append(url)
        else:
            data["queries"] = [url]

    with open(parent_dir.joinpath("data.json"), "w") as f:
        json.dump(data, f)
    bot.send_message(msg.chat.id, "✅ Добавлено")


@bot.message_handler(commands=["queries"])
def query_list(msg):
    queries = []
    with open(parent_dir.joinpath("data.json"), "r") as f:
        j = json.load(f)
        if "queries" in j:
            queries = j["queries"]

    if not queries:
        bot.send_message(msg.chat.id, "🛸 Список запросов пуст...")
        return

    message = "🔎 *Список запросов:*\n"
    line = "\n  {i}. {query}"
    for i, query in enumerate(queries):
        message += line.format(i=i, query=query)

    bot.send_message(msg.chat.id, message, parse_mode="Markdown")

@bot.message_handler(commands=["deletequery"])
def delete_query(msg):
    if msg.text.split()[1:] == [] or not msg.text.split()[1:][0].isnumeric():
        bot.send_message(msg.chat.id, "⛔ Нужно написать индекс запроса!")
        return

    index = int(msg.text.split()[1:][0])
    j = {}
    queries = []
    with open(parent_dir.joinpath("data.json"), "r") as f:
        j = json.load(f)
        if "queries" in j:
            queries = j["queries"]

    if not queries:
        bot.send_message(msg.chat.id, "🛸 Список запросов пуст...")
        return

    j["queries"].pop(index)
    with open(parent_dir.joinpath("data.json"), "w") as f:
        json.dump(j, f)

    bot.send_message(msg.chat.id, "✅ Запрос удален")
    query_list(msg)

@bot.message_handler(commands=["settimer"])
def set_timer(msg):
    if msg.text.split()[1:] == [] or not msg.text.split()[1:][0].isnumeric():
        bot.send_message(msg.chat.id, "⛔ Нужно указать время!")
        return
    j = {}
    with open(parent_dir.joinpath("data.json"), "r") as f:
        j = json.load(f)
        if "search_timer" in j:
            j["search_timer"] = int(msg.text.split[1:][0])

    with open(parent_dir.joinpath("data.json"), "w") as f:
        json.dump(j, f)

    bot.send_message(msg.chat.id, "✅ Таймер изменен на {t} секунд".format(t=msg.text.split[1:][0]))

@bot.message_handler(commands=["enable"])
def enable(msg):
    j = {}
    with open(parent_dir.joinpath("data.json"), "r") as f:
        j = json.load(f)

    j["buy_flag"] = "True"
    with open(parent_dir.joinpath("data.json"), "w") as f:
        json.dump(j, f)

    bot.send_message(msg.chat.id, "✅ Покупка включена")


@bot.message_handler(commands=["disable"])
def disable(msg):
    j = {}
    with open(parent_dir.joinpath("data.json"), "r") as f:
        j = json.load(f)

    j["buy_flag"] = "False"
    with open(parent_dir.joinpath("data.json"), "w") as f:
        json.dump(j, f)

    bot.send_message(msg.chat.id, "✅ Покупка выключена")


@bot.message_handler(commands=["ping"])
def ping(msg):
    bot.reply_to(msg, "pong")




bot.infinity_polling()
