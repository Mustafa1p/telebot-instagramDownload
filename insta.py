import telebot
import instaloader

bot = telebot.TeleBot("YOUR_TOKEN")
loader = instaloader.Instaloader()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Instagram downloader bot! Please send me the username.")

@bot.message_handler(func=lambda message: True)
def ask_download_type(message):
    chat_id = message.chat.id
    username = message.text
    bot.reply_to(message, "What would you like to download?\n1. All Posts\n2. Reels")

    @bot.message_handler(func=lambda message: True)
    def download_selected_content(message):
        content_type = message.text.lower()
        try:
            profile = instaloader.Profile.from_username(loader.context, username)
            if content_type == '1' or content_type == 'all posts':
                for post in profile.get_posts():
                    if post.typename == 'GraphVideo':
                        bot.send_video(chat_id, post.video_url)
                    elif post.typename == 'GraphImage':
                        bot.send_photo(chat_id, post.url)
            elif content_type == '2' or content_type == 'reels':
                for post in profile.get_posts():
                    if post.typename == 'GraphVideo':
                        bot.send_video(chat_id, post.video_url)
                    elif post.typename == 'GraphImage':
                        bot.send_photo(chat_id, post.url)

            bot.send_message(chat_id, "Content sent successfully!")
        except Exception as e:
            bot.send_message(chat_id, f"Error occurred: {str(e)}")

    bot.register_next_step_handler(message, download_selected_content)

bot.polling()
