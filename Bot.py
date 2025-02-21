import irc.bot
import time
import threading

# Ваши данные для подключения к Twitch
TWITCH_NICKNAME = 'your_twitch_username'
TWITCH_OAUTH_TOKEN = 'your_oauth_token'  # Получите токен здесь: https://twitchapps.com/tmi/
TWITCH_CHANNEL = '#your_channel_name'  # Канал, к которому подключается бот

DONATE_URL = 'https://www.donate.com'  # Ссылка на донат

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, nickname, oauth_token, channel):
        server = 'irc.chat.twitch.tv'
        port = 6667
        # Подключаемся к серверу
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.oauth_token = oauth_token
        self.channel = channel

    def on_welcome(self, connection, event):
        # Подключаемся к чату
        connection.join(self.channel)
        print(f'Бот подключен к каналу {self.channel}')
        
        # Запускаем поток для отправки ссылки на донат
        threading.Thread(target=self.send_donation_link, args=(connection,)).start()
    
    def send_donation_link(self, connection):
        """Функция для отправки ссылки на донат каждые 15 минут"""
        while True:
            time.sleep(900)  # 15 минут в секундах (900 секунд)
            connection.privmsg(self.channel, f"Поддержите канал: {DONATE_URL}")
            print("Отправлена ссылка на донат!")

    def on_pubmsg(self, connection, event):
        # Обрабатываем сообщение в чате
        message = event.arguments[0]
        user = event.source.nick

        # Проверяем команду !hello
        if message.lower() == '!hello':
            connection.privmsg(self.channel, f'Привет, {user}!')
        
        # Добавьте другие команды здесь, если нужно

if __name__ == "__main__":
    bot = TwitchBot(TWITCH_NICKNAME, TWITCH_OAUTH_TOKEN, TWITCH_CHANNEL)
    bot.start()
