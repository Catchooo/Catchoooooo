import telebot
from telebot import types

BOT_TOKEN = "bot_token"
bot = telebot.TeleBot(BOT_TOKEN)

bold_italic_alphabet = {
    'a': '𝗮', 'b': '𝗯', 'c': '𝗰', 'd': '𝗱', 'e': '𝗲',
    'f': '𝗳', 'g': '𝗴', 'h': '𝗵', 'i': '𝗶', 'j': '𝗷',
    'k': '𝗸', 'l': '𝗹', 'm': '𝗺', 'n': '𝗻', 'o': '𝗼',
    'p': '𝗽', 'q': '𝗾', 'r': '𝗿', 's': '𝘀', 't': '𝘁',
    'u': '𝘂', 'v': '𝘃', 'w': '𝘄', 'x': '𝘅', 'y': '𝘆',
    'z': '𝘇', ' ': ' '
}

italic_alphabet = {
  'a': '𝒂', 'b': '𝒃', 'c': '𝒄', 'd': '𝒅', 'e': '𝒆',
    'f': '𝒇', 'g': '𝒈', 'h': '𝒉', 'i': '𝒊', 'j': '𝒋',
    'k': '𝒌', 'l': '𝒍', 'm': '𝒎', 'n': '𝒏', 'o': '𝒐',
    'p': '𝒑', 'q': '𝒒', 'r': '𝒓', 's': '𝒔', 't': '𝒕',
    'u': '𝒖', 'v': '𝒗', 'w': '𝒘', 'x': '𝒙', 'y': '𝒚',
    'z': '𝒛', ' ': ' '
}

quote_alphabet = {
    'a': '𝘼', 'b': '𝘽', 'c': '𝘾', 'd': '𝘿', 'e': '𝙀',
    'f': '𝙁', 'g': '𝙂', 'h': '𝙃', 'i': '𝙄', 'j': '𝙅',
    'k': '𝙆', 'l': '𝙇', 'm': '𝙈', 'n': '𝙉', 'o': '𝙊',
    'p': '𝙋', 'q': '𝙌', 'r': '𝙍', 's': '𝙎', 't': '𝙏',
    'u': '𝙐', 'v': '𝙑', 'w': '𝙒', 'x': '𝙓', 'y': '𝙔',
    'z': '𝙓', ' ': ' '
}

text_alphabet = {
    'a': '🇦', 'b': '🇧', 'c': '🇨', 'd': '🇩', 'e': '🇪',
    'f': '🇫', 'g': '🇬', 'h': '🇭', 'i': '🇮', 'j': '🇯',
    'k': '🇰', 'l': '🇱', 'm': '🇲', 'n': '🇳', 'o': '🇴',
    'p': '🇵', 'q': '🇶', 'r': '🇷', 's': '🇸', 't': '🇹',
    'u': '🇺', 'v': '🇻', 'w': '🇼', 'x': '🇽', 'y': '🇾',
    'z': '🇿', ' ': ' '
}

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Так", callback_data="yes"),
               types.InlineKeyboardButton("Ні", callback_data="no"))
    bot.send_message(message.chat.id, "Бажаєте прокачати свій текст?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["yes", "no"])
def callback_query(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, "Напишіть свій текст:")
        bot.register_next_step_handler(call.message, process_text)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Добре, до побачення!")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

@bot.message_handler(func= lambda message: True)
def process_text(message):
    text = message.text
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("𝘁𝗲𝘅𝘁", callback_data="bold_italic"),
               types.InlineKeyboardButton("𝒕𝒆𝒙𝒕", callback_data="italic"),
               types.InlineKeyboardButton("𝙏𝙚𝙭𝙩", callback_data="quote"),
               types.InlineKeyboardButton("🇹‌🇪‌🇽‌🇹", callback_data="text"))
    bot.send_message(message.chat.id, f"Оберіть шрифт для тексту: {text}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["bold_italic", "italic", "quote", "text"])
def process_style(call):
    text = call.message.text.split(':')[1].strip()
    styled_text = ''
    alphabet = {
        'bold_italic': bold_italic_alphabet,
        'italic': italic_alphabet,
        'quote': quote_alphabet,
        'text': text_alphabet
    }[call.data]
    for char in text:
        styled_text += alphabet.get(char.lower(), char)
    bot.send_message(call.message.chat.id, f"{styled_text}", parse_mode='HTML')
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

bot.polling()
