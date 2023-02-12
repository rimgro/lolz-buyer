import logging
import os
import time

from config import Config
from market import MarketAPI, MarketBuyError, MarketItem
from market.api import parse_search_data
from telegram.telegram_bot import TelegramBot
import schedule
import datetime
from pathlib import Path
import json

TELEGRAM_MESSAGE = (
    '👷 Приобретен аккаунт: <a href="https://lzt.market/{item_id}">'
    "{title}</a>\n"
    "💲 Цена: <code>{price}₽</code>\n"
    '👷 Продавец: <a href="https://zelenka.guru/members/{seller_id}">'
    "{seller_username}</a>"
)


def conf() -> dict:
    with open(parent_dir.joinpath("data.json"), "r") as f:
        j = json.load(f)
    return j


def get_attr(j, name, default):
    if name in j:
        return j[name]
    else:
        return default


def check_accounts():
    global bought_accounts
    c = conf()
    max_acc = get_attr(c, "account_max_count", 0)
    buy_flag = get_attr(c, "buy_flag", "True") == "True"
    if not buy_flag:
        return

    # last_check = datetime.datetime.now()
    for query, params in queries:
        search_result = market.search(query, params)
        items = search_result.get("items", [])

        logging.info(
            "По запросу %s с параметрами %s найдено %s аккаунтов",
            query,
            params,
            len(items),
        )

        for item in items:
            item_id = item["item_id"]
            market_item = MarketItem(item, lolzteam_token)
            try:
                logging.info("Покупаю аккаунт %s", item_id)
                market_item.fast_buy()
            except MarketBuyError as error:
                logging.warning(
                    "При попытке покупки аккаунта %s произошла ошибка: %s",
                    item_id,
                    error.message,
                )
                continue
            else:
                logging.info("Аккаунт %s успешно куплен!", item_id)
                bought_accounts += 1

                account_object = market_item.item_object
                seller = account_object["seller"]
                data = {
                    "item_id": item_id,
                    "title": account_object["title"],
                    "price": account_object["price"],
                    "link": "https://lzt.market/{id}".format(id=item_id)
                }
                tbot.send_buy_notification(data)
                if bought_accounts >= max_acc:
                    tbot.send_message(
                        "Успешно куплено {b} аккаунтов, работа завершена.".format(b=bought_accounts)
                    )
                    c["buy_flag"] = "False"
                    with open(parent_dir.joinpath("data.json"), "w") as f:
                        json.dump(c, f)
                    bought_accounts = 0
                    break

    search_cd = get_attr(c, "search_timer", 60)
    schedule.clear("lolz")
    schedule.every(search_cd).seconds.do(check_accounts).tag("lolz")


parent_dir = Path(os.path.abspath(__file__)).parent.parent.absolute()
config = Config.load_config(parent_dir.joinpath("config.ini"))
logging.basicConfig(
    level=config.logging.level,
    format=config.logging.format,
)
lolzteam_token = config.lolzteam.token

market = MarketAPI(lolzteam_token)
queries = []
bought_accounts = 0
last_check = None
json_data = conf()

chat_id = json_data["chat_id"]
account_max_count = json_data["account_max_count"]
tbot = TelegramBot(config.telegram.bot_token, chat_id)

for search_url in get_attr(json_data, "queries", []):
    category, params = parse_search_data(search_url)
    queries.append((category, params))

search_timer = json_data["search_timer"]
tbot.send_message("Сервис покупки запущен")
schedule.every(search_timer).seconds.do(check_accounts).tag("lolz")

while True:
    schedule.run_pending()
    time.sleep(1)
