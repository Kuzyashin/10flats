import telebot
import logging
import json
from .corelogic import new_user, extract_unique_code, start_search_format, continue_search_format, \
    start_search, search_city, choose_property_type, start_search_region, continue_search_region, \
    select_cash, select_min_price, continue_select_complex_environment, process_min, process_max, \
    search_distance_to_school, search_distance_to_parks, search_distance_to_pharmacy, \
    search_distance_to_night_life, search_distance_to_markets, search_calculate
import os
from .templates import STEP_5_1_TEXT, STEP_5_2_TEXT


logger = logging.getLogger(__name__)

bot = telebot.TeleBot(os.environ['TG_BOT_TOKEN'])

if not bot.get_webhook_info().url \
        or bot.get_webhook_info().url != os.environ['TG_WEB_HOOK_ADDRESS'] + os.environ['TG_BOT_TOKEN'] + '/':
    try:
        bot.delete_webhook()
        bot.set_webhook(url=os.environ['TG_WEB_HOOK_ADDRESS'] + os.environ['TG_BOT_TOKEN'] + '/')
    except Exception as e:
        logger.warning(e)


def parse_message(request):
    json_data = request.body.decode("utf-8")
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])


def clear_keyboard(call):
    bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                  message_id=call.message.message_id,
                                  reply_markup=[])


def delete_call_message(call):
    bot.delete_message(chat_id=call.from_user.id,
                       message_id=call.message.message_id)


@bot.message_handler(commands=['start'])
def on_start(message):
    logger.info('New start command from user_id {}'.format(message.chat.id))
    unique_code = extract_unique_code(message.text)
    new_user(message, unique_code)


@bot.message_handler(func=lambda message: message.reply_to_message.text == STEP_5_1_TEXT)
def process_min_price(message):
    process_min(message)


@bot.message_handler(func=lambda message: message.reply_to_message.text == STEP_5_2_TEXT)
def process_min_price(message):
    process_max(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = json.loads(call.data)
    button = data.get('btn', None)
    step = data.get('st', None)
    if button == 'start_search':
        start_search(call)
    elif step == '1_1':
        choose_property_type(call)
    elif step == '2':
        search_city(call)
    elif step == '3':
        start_search_region(call)
    elif step == '3_1':
        continue_search_region(call)
    elif step == '4':
        start_search_format(call)
    elif step == '4_1':
        continue_search_format(call)
    elif step == '5':
        select_cash(call)
    elif step == '5_1':
        select_min_price(call)
    elif step == '6_1':
        continue_select_complex_environment(call)
    elif step == '7':
        search_distance_to_school(call)
    elif step == '8':
        search_distance_to_parks(call)
    elif step == '9':
        search_distance_to_pharmacy(call)
    elif step == '10':
        search_distance_to_night_life(call)
    elif step == '11':
        search_distance_to_markets(call)
    elif step == '12':
        search_calculate(call)

    elif button == 'read_reviews':
        pass
    elif button == 'write_review':
        pass
    elif button == 'place_advertise':
        pass
    elif button == 'download_list':
        pass
    elif button == 'download_analytics':
        pass
    elif button == 'empty_button':
        pass
    elif button == 'last_searches':
        pass
    elif button == 'change_language':
        pass
    elif button == 'support':
        pass
    else:
        pass
