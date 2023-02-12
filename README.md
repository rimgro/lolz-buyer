# lolz-auto-buyer
Данный скрипт предназначен для автоматического поиска и покупки аккаунтов с маркета https://lzt.market.

Для его запуска вам потребуется Windows/Linux, а также установленный Python 3.8+. **Никакие библиотеки предустанавливать не нужно**.

# Config.ini
Первым делом, вам нужно правильно заполнить конфигурационный файл. Вы должны открыть файл `config.example.ini` и заполнить все его поля. Дальше, вам остается изменить имя файла на `config.ini`. Поговорим о полях самого конфига:

## Lolzteam
```
token = 31156ccaff01dad7610dd6d4409d1593cd94cd9f
search_urls_list = https://lzt.market/steam/?order_by=price_to_up, https://lzt.market/discord/?order_by=price_to_up&pmax=10
count = 1
```
`token` - Токен от аккаунта Lolzteam.<br>
`search_urls_list` - Ссылки, по которым скрипт будет искать и покупать аккаунты. Чтобы ее получить, вам нужно выставить нужные параметры в [поиске маркета](https://lzt.market) и просто скопировать ссылку из адресной строки (видоизменять её **не** нужно).<br>
`count` - Количество аккаунтов, которое будет куплено. После превышения данного числа скрипт закончит работу.
## Telegram
```
[telegram]
bot_token = 1:AAABBBCCC
id = 1 # Your Telegram ID
```
`bot_token` - Токен от Telegram бота, который будет уведомлять вас о покупке аккаунта.<br>
`telegram_id` - Telegram ID, на который будет отправляться уведомление о покупке аккаунта.<br>
## Logging
**Не трогайте данный раздел, если вы не являетесь разработчиком.**
```
level = 20
format = [%%(levelname)s] %%(asctime)s - %%(name)s - %%(message)s
```
`level` - Уровень логирования. <br>
`format` - Формат логов. (Из-за особенностей файла .ini символ '%' нужно экранировать)

# Как его запустить?

И так, вы правильно заполнили файл config.ini, отлично! Теперь, осталось запустить скрипт, для этого используйте команду:
```bash
python -m buyservice
```
Ключевое слово `python` может меняться в зависимости от версии самого Python и от вашей операционной системы.

Теперь скрипт работает! Каждые 3 секунды он проверяет аккаунты на маркете по вашему запросу, и если такие находятся - покупает их. О покупке он сообщает вам в личные сообщения Telegram от имени бота, токен от которого вы указали в config.ini.


# FAQ
Q - Как получить токен Lolzteam?<br>
A - Для этого вам нужно перейти по [ссылке](https://zelenka.guru/account/authorize?client_id=v3fqcys6di&response_type=token&scope=market+read+post). После выдачи разрешения, вас перенаправит на этот же репозиторий. Вам будет достаточно скопировать значение параметра `access_token` из адресной строки браузера.
![Взято из https://zelenka.guru/posts/comments/8086747](https://i.imgur.com/KLriwYl.png)

Q - Можно ли вставить несколько запросов в скрипт? <br>
A - Да. Для этого вам нужно перечислить ссылки на покупку через запятую.

Q - Можно ли уменьшить задержку между запросами? <br>
A - Нет, это ограничение идет со стороны Market API и обойти его никак нельзя.