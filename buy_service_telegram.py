import time

import schedule
from telebot import TeleBot, types
from telebot.formatting import escape_markdown
import asyncio


class TelegramBot:
    def __init__(self, token, chat_id):
        self.bot = TeleBot(token)
        self.chat_id = chat_id

    # def send_main_menu(self, chat_id):
    #     menu_text = "*🟢 LZT AUTO FARMER*\n" \
    #                 "\n" \
    #                 "✅ Работает\n" \
    #                 "💵 Куплено {bought_accounts}/{buy_limit} аккаунтов \n" \
    #                 "🛸 Загружено {filter_count} фильтров\n" \
    #                 "🔥 Последняя проверка: {last_check} ".format(bought_accounts=self.main.bought_accounts,
    #                                                               buy_limit=self.main.config.lolzteam.count,
    #                                                               filter_count=len(self.main.queries),
    #                                                               last_check=self.main.last_check)
    #
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     markup.row("Добавить запрос")
    #     markup.row("Запросы", "Статистика")
    #     markup.row("Остановить бота", "Настройки")
    #
    #     self.main_menu = self.bot.send_message(chat_id, menu_text, reply_markup=markup, parse_mode="Markdown")
    #
    # def delete_notification(self, msg, wait):
    #     time.sleep(wait)
    #     self.bot.delete_message(msg.chat.id, msg.id)

    def send_message(self, message):
        self.bot.send_message(self.chat_id, message)
    #
    # async def run_bot(self):
    #     await self.bot.polling()

    def send_buy_notification(self, data):
        notification = "📢 *Куплен аккаунт* \n\n" \
                       "*Название*: {title}\n" \
                       "*Цена*: {price}\n" \
                       "*Категория*: TODO\n" \
                       "\n" \
                       "{link}".format(link=data["link"], price=data["price"], account_type=data["account_type"],
                                       title=data["title"])
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("Посмотреть аккаунт", url=data["link"]),
                     types.InlineKeyboardButton("Продать аккаунт (когда?)"))
        self.bot.send_message(self.chat_id, notification, parse_mode="Markdown")
