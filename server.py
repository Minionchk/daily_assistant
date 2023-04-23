import logging
from telegram.ext import Application, ApplicationBuilder, CommandHandler, \
    MessageHandler, filters
from telegram.ext import Updater, CommandHandler
from telegram import ReplyKeyboardMarkup
import random
import requests
from translate import Translator
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)
proxy_url = "socks5://user:pass@host:port"
app = ApplicationBuilder().token("6036569426:AAEp_CH_gNaJ8WSDmGpDvbCrCUVlc4sNBO4").proxy_url(
    proxy_url).build()
reply_keyboard = [['/help', '/joke'],
                  ['/weather', '/horoscope'],
                  ['/todo_list_check', '/todo_list_add', '/todo_list_clear']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот-ежедневник, для друзей просто Ди. Можешь написать "
        "мне в любой момент, а я помогу как смогу! С помощью команды /help "
        "ты можешь увидеть что я могу", reply_markup=markup)


async def help_command(update, context):
    await update.message.reply_text("/joke - отправить анекдот сгенерированный ChatGPT фтоооо?!"
                                    " \n /weather - отправить погоду на сегодня "
                                    "\n /horoscope - отправить гороскопы на сегодня"
                                    "\n /todo_list_add - создать список дел и добавить"
                                    " в него элемент"
                                    "\n /todo_list_check - посмотреть список дел"
                                    "\n /todo_list_clear - очистить список дел",
                                    reply_markup=markup)


async def log(update, context):
    f = open('log.txt', 'r+', encoding='utf-8')
    f.seek(0, 2)
    print(update.message.text, file=f)


async def jokes(update, context):
    f = open("jokes.txt", encoding="utf-8").readlines()
    line = random.choice(f)
    await update.message.reply_text(line)


async def todo_list_add(update, context):
    f = open("todo_list.txt", mode="w", encoding="utf-8")
    await update.message.reply_text("Введите дело, которое хотите добавить, "
                                    "а затем команду /todo_list_add2")


async def todo_list_add2(update, context):
    f1 = open("todo_list.txt", mode="r+", encoding="utf-8")
    task = open('log.txt', mode='r', encoding='utf-8').readlines()[-1]
    f1.seek(0, 2)
    print(task, file=f1)
    await update.message.reply_text("Дело добавлено!")


async def todo_list_check(update, context):
    lines = open('todo_list.txt', mode='r', encoding='utf-8').readlines()
    s = ''
    for line in lines:
        s += line
    if s:
        await update.message.reply_text("Список дел: \n" + s)
    else:
        await update.message.reply_text("Список пуст")


async def todo_list_clear(update, context):
    f = open('todo_list.txt', mode='w')
    f.write('')
    await update.message.reply_text("Список дел очищен!")


async def weather(update, context):
    translator = Translator(from_lang="English", to_lang="russian")
    res = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?lat=55.718671&lon="
        "37.587271&exclude=daily&appid=0df371a04f53ee43261def6e1138ae08")
    data = res.json()
    # data = json.dumps(data)
    s = f'Сегодня в Москве {translator.translate(data["weather"][0]["description"])}' \
        f'. Температура в течении дня будет от ' \
        f'{round(float(data["main"]["temp_min"]) - 273.15)}, ' \
        f'до {round(float(data["main"]["temp_max"]) - 273.15)} градусов'
    await update.message.reply_text(s)


async def horoscope(update, context):
    translator = Translator(from_lang="English", to_lang="russian")
    for i in range(0, 12):
        zodiacs = ['Aries', 'Taurus', 'Gemini',
                   'Cancer', 'Leo', 'Virgo',
                   'Libra', 'Scorpio', 'Sagittarius',
                   'Capricorn', 'Aquarius', 'Pisces']
        url = (
            "https://www.horoscope.com/us/horoscopes/general/"
            f"horoscope-general-daily-today.aspx?sign={i+1}"
        )
        soup = BeautifulSoup(requests.get(url).content,
                             "html.parser")
        await update.message.reply_text(
            zodiacs[i] + ', ' + soup.find("div", class_="main-horoscope").p.text)


def main():
    application = Application.builder().token(
        "6036569426:AAEp_CH_gNaJ8WSDmGpDvbCrCUVlc4sNBO4").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("joke", jokes))
    application.add_handler(CommandHandler("todo_list_add", todo_list_add))
    application.add_handler(CommandHandler("todo_list_add2", todo_list_add2))
    application.add_handler(CommandHandler("todo_list_check", todo_list_check))
    application.add_handler(CommandHandler("todo_list_clear", todo_list_clear))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(CommandHandler("horoscope", horoscope))
    application.add_handler(MessageHandler(filters.TEXT, log))
    application.run_polling()


if __name__ == '__main__':
    main()
