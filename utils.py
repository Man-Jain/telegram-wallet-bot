import telebot
import jinja2

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)

def serialize_table(items):
    result = ''
    for item in items:
        print(item)
        result += '<b>' + item['contract_ticker_symbol'] + '</b> -> ' + \
              str(int(item['balance']) / 10 ** 18) + ' -> ' + str(item['quote']) + "\n"

    return result

def get_back_keyboard(call_from):
   keyboard = telebot.types.InlineKeyboardMarkup()
   keyboard.row(
       telebot.types.InlineKeyboardButton('Back 🔙', callback_data='home'),
       telebot.types.InlineKeyboardButton('Refresh 🔁', callback_data='refresh' + call_from)
   )
   return keyboard

def get_defi_keyboard(call_from):
   keyboard = telebot.types.InlineKeyboardMarkup()

   keyboard.row(
       telebot.types.InlineKeyboardButton('Uniswap V2', callback_data='home'),
       telebot.types.InlineKeyboardButton('Aave', callback_data='refresh' + call_from),
   )
   keyboard.row(
       telebot.types.InlineKeyboardButton('Balancer', callback_data='refresh' + call_from),
       telebot.types.InlineKeyboardButton('Compound', callback_data='refresh' + call_from),
   )
   keyboard.row(
       telebot.types.InlineKeyboardButton('Curve', callback_data='refresh' + call_from),
       telebot.types.InlineKeyboardButton('Maker', callback_data='refresh' + call_from),
   )
   keyboard.row(
       telebot.types.InlineKeyboardButton('Back 🔙', callback_data='home'),
   )
   return keyboard

def getHTML(type, data):
    TEMPLATE_FILE = 'templates/' + type + '.html'
    template = templateEnv.get_template(TEMPLATE_FILE)
    output = template.render(data=data)
    return output