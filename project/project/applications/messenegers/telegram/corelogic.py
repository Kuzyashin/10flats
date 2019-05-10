# -*- coding: utf-8 -*-
import json
import logging

import telebot
from django.utils import timezone

from core.models import Currency, DistanceMatrix
from messenegers.models import TelegramUser
import os
from properites.models import City, Area, PropertyType, PropertyFormat
from realty.models import RealtyObject
from searchengine.models import Search, DistanceChoose
from .templates import *

logger = logging.getLogger(__name__)
bot = telebot.TeleBot(os.environ['TG_BOT_TOKEN'])


def extract_unique_code(text):
    logger.info('Extracting unique code')
    return text.split()[1] if len(text.split()) > 1 else None


def get_beautiful_username(tg_user):
    tg_user = TelegramUser.objects.get(pk=tg_user.pk)
    try:
        if tg_user.telegram_username:
            return '#' + str(tg_user.pk) + '  @' + tg_user.telegram_username
        else:
            return tg_user.first_name + ' #' + str(tg_user.pk)
    except Exception as e:
        logger.warning(e)


def new_user(message, unique_code):
    if unique_code:
        refer_tag = unique_code.split('-')[0]
    else:
        refer_tag = None
    try:
        telegram_user = TelegramUser.objects.get(telegram_chat_id=message.from_user.id)
    except TelegramUser.DoesNotExist:
        telegram_user = TelegramUser(
            telegram_chat_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            telegram_username=message.from_user.username,
            created_at=timezone.now(),
            referral=refer_tag,
        )
        telegram_user.save()
        if refer_tag:
            bot.send_message(os.environ['TG_ADMIN_GROUP'],
                             ADMIN_NEW_USER_REF.format(get_beautiful_username(telegram_user), refer_tag))
        else:
            bot.send_message(os.environ['TG_ADMIN_GROUP'],
                             ADMIN_NEW_USER_NOREF.format(get_beautiful_username(telegram_user)))
    reply_markup = telebot.types.InlineKeyboardMarkup()
    _start_search_button = telebot.types.InlineKeyboardButton(
        text='Запустить алгоритм поиска 🔎',
        callback_data=json.dumps({
            'btn': 'start_search',
            'telegram_user': telegram_user.pk
        })
    )
    _read_reviews_button = telebot.types.InlineKeyboardButton(
        text='Почитать отзывы жильцов 📖',
        callback_data=json.dumps({
            'btn': 'read_reviews',
            'telegram_user': telegram_user.pk
        })
    )
    _write_review_button = telebot.types.InlineKeyboardButton(
        text='Оставить отзыв о комплексе 📝',
        callback_data=json.dumps({
            'btn': 'write_review',
            'telegram_user': telegram_user.pk
        })
    )
    _place_advertise_button = telebot.types.InlineKeyboardButton(
        text='Разместить объявление 📜',
        callback_data=json.dumps({
            'btn': 'place_advertise',
            'telegram_user': telegram_user.pk
        })
    )
    _download_list_button = telebot.types.InlineKeyboardButton(
        text='Полный список объектов 🏙',
        callback_data=json.dumps({
            'btn': 'download_list',
            'telegram_user': telegram_user.pk
        })
    )
    _download_analytics_button = telebot.types.InlineKeyboardButton(
        text='Аналитический отчет 📊',
        callback_data=json.dumps({
            'btn': 'download_analytics',
            'telegram_user': telegram_user.pk
        })
    )
    _empty_button = telebot.types.InlineKeyboardButton(
        text='--------------------',
        callback_data=json.dumps({
            'btn': 'empty_button',
            'telegram_user': telegram_user.pk
        })
    )
    _last_searches_button = telebot.types.InlineKeyboardButton(
        text='История поисков 🕐',
        callback_data=json.dumps({
            'btn': 'last_searches',
            'telegram_user': telegram_user.pk
        })
    )
    _change_language_button = telebot.types.InlineKeyboardButton(
        text='Язык / Language 🔠',
        callback_data=json.dumps({
            'btn': 'change_language',
            'telegram_user': telegram_user.pk
        })
    )
    _support_button = telebot.types.InlineKeyboardButton(
        text='Поддержки / Support ❓',
        callback_data=json.dumps({
            'btn': 'support',
            'telegram_user': telegram_user.pk
        })
    )
    reply_markup.add(_start_search_button)
    reply_markup.add(_read_reviews_button)
    reply_markup.add(_write_review_button)
    reply_markup.add(_place_advertise_button)
    reply_markup.add(_download_list_button)
    reply_markup.add(_download_analytics_button)
    reply_markup.add(_empty_button)
    reply_markup.add(_last_searches_button)
    reply_markup.add(_change_language_button)
    reply_markup.add(_support_button)

    bot.send_message(
        chat_id=telegram_user.telegram_chat_id,
        text=START_TEXT,
        reply_markup=reply_markup
    )


def start_search(call):
    data = json.loads(call.data)
    telegram_user = TelegramUser.objects.get(pk=data.get('telegram_user'))
    new_search = Search.objects.create(
        telegram_user=telegram_user,
        last_step=1,
        created_at=timezone.now(),
    )
    new_search.save()
    step_text = STEP_1_TEXT
    reply_markup = telebot.types.InlineKeyboardMarkup()
    _search_buy_button = telebot.types.InlineKeyboardButton(
        text='Покупка',
        callback_data=json.dumps({
            'btn': 'search_buy',
            'st': '1_1',
            's': new_search.pk,
        })
    )
    _search_rent_button = telebot.types.InlineKeyboardButton(
        text='Аренда',
        callback_data=json.dumps({
            'btn': 'search_rent',
            'st': '1_1',
            's': new_search.pk,
        })
    )
    reply_markup.add(
        _search_buy_button, _search_rent_button
    )
    bot.edit_message_text(
        chat_id=telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        text=step_text
    )
    bot.edit_message_reply_markup(
        chat_id=telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        reply_markup=reply_markup
    )


def choose_property_type(call):
    data = json.loads(call.data)
    search = Search.objects.get(pk=data.get('s'))
    step_text = STEP_1_1_TEXT
    search.last_step = '1_1'
    search.progress = json.dumps({
        'step_1': data.get('btn')
    })
    search.save()
    property_types = PropertyType.objects.all()
    reply_markup = telebot.types.InlineKeyboardMarkup()
    for property_type in property_types:
        _property_type_button = telebot.types.InlineKeyboardButton(
            text='{}'.format(property_type.type),
            callback_data=json.dumps({
                'btn': 'property_type',
                'st': '2',
                'tp': property_type.pk,
                's': search.pk,
            })
        )
        reply_markup.add(_property_type_button)
    bot.edit_message_text(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        text=step_text
    )
    bot.edit_message_reply_markup(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        reply_markup=reply_markup
    )


def search_city(call):
    data = json.loads(call.data)
    search = Search.objects.get(pk=data.get('s'))
    step_text = STEP_2_TEXT
    reply_markup = telebot.types.InlineKeyboardMarkup()
    progress = json.loads(search.progress)
    progress.update({'step_1_1': data.get('tp')})
    search.progress = json.dumps(progress)
    search.last_step = '2'
    search.save()
    city_list = City.objects.all()
    for city in city_list:
        _city_name_button = telebot.types.InlineKeyboardButton(
            text='{}'.format(city.city),
            callback_data=json.dumps({
                'btn': 'city',
                'st': '3',
                'tp': city.pk,
                's': search.pk,
            })
        )
        reply_markup.add(_city_name_button)
    bot.edit_message_text(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        text=step_text
    )
    bot.edit_message_reply_markup(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        reply_markup=reply_markup
    )


def start_search_region(call):
    data = json.loads(call.data)
    search = Search.objects.get(pk=data.get('s'))
    step_text = STEP_3_TEXT
    reply_markup = telebot.types.InlineKeyboardMarkup()
    progress = json.loads(search.progress)
    progress.update({'step_2': data.get('tp')})
    search.progress = json.dumps(progress)
    search.last_step = '3'
    search.save()
    regions = Area.objects.all()
    for region in regions:
        _region_name_button = telebot.types.InlineKeyboardButton(
            text='{}'.format(region.area),
            callback_data=json.dumps({
                'btn': 'region_add',
                'st': '3_1',
                'tp': region.pk,
                's': search.pk,
            })
        )
        reply_markup.add(_region_name_button)
    bot.edit_message_text(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        text=step_text
    )
    bot.edit_message_reply_markup(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        reply_markup=reply_markup
    )


def continue_search_region(call):
    data = json.loads(call.data)
    search = Search.objects.get(pk=data.get('s'))
    reply_markup = telebot.types.InlineKeyboardMarkup()
    progress = json.loads(search.progress)
    region_list = []
    if data.get('btn') == 'region_add':
        if progress.get('step_3', None):
            region_list = progress.get('step_3')
            if data.get('tp') not in region_list:
                region_list.append(data.get('tp'))
                progress.update({'step_3': region_list})
        else:
            progress.update({'step_3': [data.get('tp')]})
            region_list = [data.get('tp')]
    elif data.get('btn') == 'region_rmv':
        region_list = progress.get('step_3')
        region_list.remove(data.get('tp'))
    search.progress = json.dumps(progress)
    search.last_step = '3_1'
    search.save()
    regions = Area.objects.all()
    for region in regions:
        if region.pk in region_list:
            _ok_region_name_button = telebot.types.InlineKeyboardButton(
                text='{} ✅'.format(region.area),
                callback_data=json.dumps({
                    'btn': 'region_rmv',
                    'st': '3_1',
                    'tp': region.pk,
                    's': search.pk,
                })
            )
            reply_markup.add(_ok_region_name_button)
        else:
            _region_name_button = telebot.types.InlineKeyboardButton(
                text='{}'.format(region.area),
                callback_data=json.dumps({
                    'btn': 'region_add',
                    'st': '3_1',
                    'tp': region.pk,
                    's': search.pk,
                })
            )
            reply_markup.add(_region_name_button)
    _region_continue_button = telebot.types.InlineKeyboardButton(
        text='Продолжить ➡️',
        callback_data=json.dumps({
            'btn': 'region',
            'st': '4',
            'tp': region_list,
            's': search.pk,
        })
    )
    reply_markup.add(_region_continue_button)
    bot.edit_message_reply_markup(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        reply_markup=reply_markup
    )


def start_search_format(call):
    data = json.loads(call.data)
    search = Search.objects.get(pk=data.get('s'))
    step_text = STEP_4_TEXT
    reply_markup = telebot.types.InlineKeyboardMarkup()
    search.last_step = '4'
    search.save()
    formats = PropertyFormat.objects.all().order_by('type')
    for property_format in formats:
        _region_name_button = telebot.types.InlineKeyboardButton(
            text='{}'.format(property_format.type),
            callback_data=json.dumps({
                'btn': 'add',
                'st': '4_1',
                'tp': property_format.pk,
                's': search.pk,
            })
        )
        reply_markup.add(_region_name_button)
    bot.edit_message_text(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        text=step_text
    )
    bot.edit_message_reply_markup(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        reply_markup=reply_markup
    )


def continue_search_format(call):
    data = json.loads(call.data)
    search = Search.objects.get(pk=data.get('s'))
    reply_markup = telebot.types.InlineKeyboardMarkup()
    progress = json.loads(search.progress)
    formats_list = []
    if data.get('btn') == 'add':
        if progress.get('step_4', None):
            formats_list = progress.get('step_4')
            if data.get('tp') not in formats_list:
                formats_list.append(data.get('tp'))
                progress.update({'step_4': formats_list})
        else:
            progress.update({'step_4': [data.get('tp')]})
            formats_list = [data.get('tp')]
    elif data.get('btn') == 'rmv':
        formats_list = progress.get('step_4')
        formats_list.remove(data.get('tp'))
    search.progress = json.dumps(progress)
    search.last_step = '4_1'
    search.save()
    formats = PropertyFormat.objects.all().order_by('type')
    for property_format in formats:
        if property_format.pk in formats_list:
            _ok_format_name_button = telebot.types.InlineKeyboardButton(
                text='{} ✅'.format(property_format.type),
                callback_data=json.dumps({
                    'btn': 'rmv',
                    'st': '4_1',
                    'tp': property_format.pk,
                    's': search.pk,
                })
            )
            reply_markup.add(_ok_format_name_button)
        else:
            _format_name_button = telebot.types.InlineKeyboardButton(
                text='{}'.format(property_format.type),
                callback_data=json.dumps({
                    'btn': 'add',
                    'st': '4_1',
                    'tp': property_format.pk,
                    's': search.pk,
                })
            )
            reply_markup.add(_format_name_button)
    _format_continue_button = telebot.types.InlineKeyboardButton(
        text='Продолжить ➡️',
        callback_data=json.dumps({
            'btn': 'frm',
            'st': '5',
            's': search.pk,
        })
    )
    reply_markup.add(_format_continue_button)
    bot.edit_message_reply_markup(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        reply_markup=reply_markup
    )


def select_cash(call):
    data = json.loads(call.data)
    search = Search.objects.get(pk=data.get('s'))
    step_text = STEP_5_TEXT
    reply_markup = telebot.types.InlineKeyboardMarkup()
    search.last_step = '5'
    search.save()
    currency_list = Currency.objects.all()
    for currency in currency_list:
        _currency_name_button = telebot.types.InlineKeyboardButton(
            text='{} - {}'.format(currency.code, currency.name),
            callback_data=json.dumps({
                'btn': 'curr',
                'st': '5_1',
                'tp': currency.pk,
                's': search.pk,
            })
        )
        reply_markup.add(_currency_name_button)
    bot.edit_message_text(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        text=step_text
    )
    bot.edit_message_reply_markup(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        reply_markup=reply_markup
    )


def process_min(message):
    search = Search.objects.get(min_price_msg=message.reply_to_message.message_id)
    select_max_price(message, search.pk)


def process_max(message):
    search = Search.objects.get(max_price_msg=message.reply_to_message.message_id)
    start_select_complex_environment(message, search.pk)


def select_min_price(call):
    data = json.loads(call.data)
    search = Search.objects.get(pk=data.get('s'))
    step_text = STEP_5_1_TEXT
    bot.delete_message(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
    )
    msg_id = bot.send_message(
        chat_id=search.telegram_user.telegram_chat_id,
        text=step_text,
        reply_markup=telebot.types.ForceReply()
    ).message_id
    progress = json.loads(search.progress)
    progress.update({'step_5': data.get('tp')})
    search.progress = json.dumps(progress)
    search.last_step = '5_1'
    search.min_price_msg = msg_id
    search.save()


def select_max_price(message, s_pk):
    search = Search.objects.get(pk=s_pk)
    step_text = STEP_5_2_TEXT
    bot.delete_message(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=message.reply_to_message.message_id,
    )
    msg_id = bot.send_message(
        chat_id=search.telegram_user.telegram_chat_id,
        text=step_text,
        reply_markup=telebot.types.ForceReply()
    ).message_id
    progress = json.loads(search.progress)
    progress.update({'step_5_1': message.text})
    search.progress = json.dumps(progress)
    search.last_step = '5_2'
    search.max_price_msg = msg_id
    search.save()


def start_select_complex_environment(message, s_pk):
    pass

def continue_select_complex_environment(call):
    pass


#TODO: Normalno sdelat eto govno
"""
def start_select_complex_environment(message, s_pk):
    search = Search.objects.get(pk=s_pk)
    step_text = STEP_6_TEXT
    bot.delete_message(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=message.reply_to_message.message_id,
    )
    progress = json.loads(search.progress)
    progress.update({'step_5_2': message.text})
    search.progress = json.dumps(progress)
    search.last_step = '6'
    search.save()
    reply_markup = telebot.types.InlineKeyboardMarkup()
    environments = ComplexEnvironment.objects.filter(is_active=True)
    for env_type in environments:
        _env_name_button = telebot.types.InlineKeyboardButton(
            text='{}'.format(env_type.name),
            callback_data=json.dumps({
                'btn': 'add',
                'st': '6_1',
                'tp': env_type.pk,
                's': search.pk,
            })
        )
        reply_markup.add(_env_name_button)
    bot.delete_message(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=message.message_id,
    )
    bot.send_message(
        chat_id=search.telegram_user.telegram_chat_id,
        text=step_text,
        reply_markup=reply_markup
    )


def continue_select_complex_environment(call):
    data = json.loads(call.data)
    search = Search.objects.get(pk=data.get('s'))
    reply_markup = telebot.types.InlineKeyboardMarkup()
    progress = json.loads(search.progress)
    env_list = []
    if data.get('btn') == 'add':
        if progress.get('step_6', None):
            env_list = progress.get('step_6')
            if data.get('tp') not in env_list:
                env_list.append(data.get('tp'))
                progress.update({'step_6': env_list})
        else:
            progress.update({'step_6': [data.get('tp')]})
            env_list = [data.get('tp')]
    elif data.get('btn') == 'rmv':
        env_list = progress.get('step_6')
        env_list.remove(data.get('tp'))
    search.progress = json.dumps(progress)
    search.last_step = '6_1'
    search.save()
    envs = ComplexEnvironment.objects.filter(is_active=True)
    for env_format in envs:
        if env_format.pk in env_list:
            _ok_env_name_button = telebot.types.InlineKeyboardButton(
                text='{} ✅'.format(env_format.name),
                callback_data=json.dumps({
                    'btn': 'rmv',
                    'st': '6_1',
                    'tp': env_format.pk,
                    's': search.pk,
                })
            )
            reply_markup.add(_ok_env_name_button)
        else:
            _env_name_button = telebot.types.InlineKeyboardButton(
                text='{}'.format(env_format.name),
                callback_data=json.dumps({
                    'btn': 'add',
                    'st': '6_1',
                    'tp': env_format.pk,
                    's': search.pk,
                })
            )
            reply_markup.add(_env_name_button)
    _env_continue_button = telebot.types.InlineKeyboardButton(
        text='Продолжить ➡️',
        callback_data=json.dumps({
            'btn': 'envs',
            'st': '7',
            's': search.pk,
        })
    )
    reply_markup.add(_env_continue_button)
    bot.edit_message_reply_markup(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        reply_markup=reply_markup
    )
"""

def search_distance_to_school(call):
    data = json.loads(call.data)
    search = Search.objects.get(pk=data.get('s'))
    reply_markup = telebot.types.InlineKeyboardMarkup()
    step_text = STEP_7_TEXT
    search.last_step = '8'
    search.save()
    for dist_btn in DistanceChoose.objects.all().order_by('distance'):
        _distance_name_button = telebot.types.InlineKeyboardButton(
            text='{}'.format(dist_btn.text),
            callback_data=json.dumps({
                'btn': 'dist',
                'st': '8',
                'tp': dist_btn.pk,
                's': search.pk,
            })
        )
        reply_markup.add(_distance_name_button)
    bot.edit_message_text(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        text=step_text
    )
    bot.edit_message_reply_markup(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        reply_markup=reply_markup
    )


def search_distance_to_parks(call):
    data = json.loads(call.data)
    search = Search.objects.get(pk=data.get('s'))
    reply_markup = telebot.types.InlineKeyboardMarkup()
    step_text = STEP_8_TEXT
    progress = json.loads(search.progress)
    progress.update({'step_7': data.get('tp')})
    search.progress = json.dumps(progress)
    search.last_step = '9'
    search.save()
    for dist_btn in DistanceChoose.objects.all().order_by('distance'):
        _distance_name_button = telebot.types.InlineKeyboardButton(
            text='{}'.format(dist_btn.text),
            callback_data=json.dumps({
                'btn': 'dist',
                'st': '9',
                'tp': dist_btn.pk,
                's': search.pk,
            })
        )
        reply_markup.add(_distance_name_button)
    bot.edit_message_text(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        text=step_text
    )
    bot.edit_message_reply_markup(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        reply_markup=reply_markup
    )


def search_distance_to_pharmacy(call):
    data = json.loads(call.data)
    search = Search.objects.get(pk=data.get('s'))
    reply_markup = telebot.types.InlineKeyboardMarkup()
    step_text = STEP_9_TEXT
    progress = json.loads(search.progress)
    progress.update({'step_8': data.get('tp')})
    search.progress = json.dumps(progress)
    search.last_step = '10'
    search.save()
    for dist_btn in DistanceChoose.objects.all().order_by('distance'):
        _distance_name_button = telebot.types.InlineKeyboardButton(
            text='{}'.format(dist_btn.text),
            callback_data=json.dumps({
                'btn': 'dist',
                'st': '10',
                'tp': dist_btn.pk,
                's': search.pk,
            })
        )
        reply_markup.add(_distance_name_button)
    bot.edit_message_text(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        text=step_text
    )
    bot.edit_message_reply_markup(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        reply_markup=reply_markup
    )


def search_distance_to_night_life(call):
    data = json.loads(call.data)
    search = Search.objects.get(pk=data.get('s'))
    reply_markup = telebot.types.InlineKeyboardMarkup()
    step_text = STEP_10_TEXT
    progress = json.loads(search.progress)
    progress.update({'step_9': data.get('tp')})
    search.progress = json.dumps(progress)
    search.last_step = '11'
    search.save()
    for dist_btn in DistanceChoose.objects.all().order_by('distance'):
        _distance_name_button = telebot.types.InlineKeyboardButton(
            text='{}'.format(dist_btn.text),
            callback_data=json.dumps({
                'btn': 'dist',
                'st': '11',
                'tp': dist_btn.pk,
                's': search.pk,
            })
        )
        reply_markup.add(_distance_name_button)
    bot.edit_message_text(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        text=step_text
    )
    bot.edit_message_reply_markup(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        reply_markup=reply_markup
    )


def search_distance_to_markets(call):
    data = json.loads(call.data)
    search = Search.objects.get(pk=data.get('s'))
    reply_markup = telebot.types.InlineKeyboardMarkup()
    step_text = STEP_11_TEXT
    progress = json.loads(search.progress)
    progress.update({'step_10': data.get('tp')})
    search.progress = json.dumps(progress)
    search.last_step = '11'
    search.save()
    for dist_btn in DistanceChoose.objects.all().order_by('distance'):
        _distance_name_button = telebot.types.InlineKeyboardButton(
            text='{}'.format(dist_btn.text),
            callback_data=json.dumps({
                'btn': 'dist',
                'st': '12',
                'tp': dist_btn.pk,
                's': search.pk,
            })
        )
        reply_markup.add(_distance_name_button)
    bot.edit_message_text(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        text=step_text
    )
    bot.edit_message_reply_markup(
        chat_id=search.telegram_user.telegram_chat_id,
        message_id=call.message.message_id,
        reply_markup=reply_markup
    )


def search_calculate(call):
    data = json.loads(call.data)
    search = Search.objects.get(pk=data.get('s'))
    reply_markup = telebot.types.InlineKeyboardMarkup()
    step_text = STEP_12_TEXT
    progress = json.loads(search.progress)
    progress.update({'step_11': data.get('tp')})
    search.progress = json.dumps(progress)
    search.last_step = '12'
    search.save()
    """
    {"step_1": "search_buy",            Покупка/аренда
     "step_1_1": 2,                     PropertyType
      "step_2": 2,                      City
       "step_3": [3],                   Area
        "step_4": [3],                  PropertyFormat
          "step_5": 1,                  Currency
           "step_5_1": "1000",          MinPrice
            "step_5_2": "0",            MaxPrice
             "step_6": [4, 1, 5],       ComplexEnvironment
              "step_7": 1,              Dist_school
               "step_8": 2,             Dist_park
                "step_9": 4,            Dist_pharm
                "step_10": 4,           Dist_night
                 "step_11": 4,          Dist_market
                }
    """
    qs = RealtyObject.objects.all().distinct()
    if progress.get('step_1') == 'search_buy':
        _step_1 = 'buy'
        qs = qs.filter(sell_available=True)
    else:
        _step_1 = 'rent'
        qs = qs.filter(rent_available=True)
    _prop_type = PropertyType.objects.get(pk=int(progress.get('step_1_1')))
    qs = qs.filter(property_type=_prop_type)
    _city = City.objects.get(pk=int(progress.get('step_2')))
    qs = qs.filter(realty_complex__area__city=_city)
    _area_list = Area.objects.filter(pk__in=progress.get('step_3'))
    qs = qs.filter(realty_complex__city__area__in=_area_list)
    _format_list = PropertyFormat.objects.filter(pk__in=progress.get('step_4'))
    qs = qs.filter(property_format__in=_format_list)
    _currency = Currency.objects.get(pk=int(progress.get('step_5')))
    _min_price_eur = int(progress.get('step_5_1')) * _currency.to_eur_price
    if _min_price_eur > 0:
        if _step_1 == 'buy':
            qs = qs.filter(selling_price_eur__gt=_min_price_eur)
        else:
            qs = qs.filter(rent_price_eur__gt=_min_price_eur)
    _max_price_eur = int(progress.get('step_5_2')) * _currency.to_eur_price
    if _max_price_eur > 0:
        if _step_1 == 'buy':
            qs = qs.filter(selling_price_eur__gt=_max_price_eur)
        else:
            qs = qs.filter(rent_price_eur__gt=_max_price_eur)

#TODO: I eto govno toze sdelat

#    _environment_list = ComplexEnvironment.objects.filter(pk__in=progress.get('step_6'))
#    for env_item in _environment_list:
#        if env_item.model_text == 'hamam':
#            qs = qs.filter(realty_complex__hamam__in=[True, None])
#        elif env_item.model_text == 'pool':
#            qs = qs.filter(realty_complex__pool__in=[True, None])
#        elif env_item.model_text == 'gym':
#            qs = qs.filter(realty_complex__gym__in=[True, None])
#        elif env_item.model_text == 'concierge':
#            qs = qs.filter(realty_complex__concierge__in=[True, None])
#        elif env_item.model_text == 'water_slides':
#            qs = qs.filter(realty_complex__water_slides__in=[True, None])

    _school_distance = DistanceChoose.objects.get(pk=progress.get('step_7'))
    _park_distance = DistanceChoose.objects.get(pk=progress.get('step_8'))
    _pharmacy_distance = DistanceChoose.objects.get(pk=progress.get('step_9'))
    _night_distance = DistanceChoose.objects.get(pk=progress.get('step_10'))
    _market_distance = DistanceChoose.objects.get(pk=progress.get('step_11'))
    """
    1 - Принципильно
    2 - не критично 
    3 - не важно
    """
    _school_percent_list = dict()
    _park_percent_list = dict()
    _pharmacy_percent_list = dict()
    _nightclub_percent_list = dict()
    _market_percent_list = dict()
    for realty_object in qs:
        try:
            _distance = realty_object.realty_complex.school_dist
            if _school_distance.distance > _distance:
                _percent = 100
            else:
                _percent = 100 - (_distance - _school_distance.distance)/_school_distance.distance*100
                if _percent < 0:
                    _percent = 0
            _school_json = {realty_object.pk: _percent}
            _school_percent_list.update(_school_json)
        except DistanceMatrix.DoesNotExist:
            print('No dist for complex {} school'.format(realty_object.realty_complex.name))
            _school_json = {realty_object.pk: 0}
            _school_percent_list.update(_school_json)
        try:
            _distance = realty_object.realty_complex.park_dist
            if _park_distance.distance > _distance:
                _percent = 100
            else:
                _percent = 100 - (_distance - _park_distance.distance) / _park_distance.distance * 100
                if _percent < 0:
                    _percent = 0
            _park_json = {realty_object.pk: _percent}
            _park_percent_list.update(_park_json)
        except DistanceMatrix.DoesNotExist:
            print('No dist for complex {} park'.format(realty_object.realty_complex.name))
            _park_json = {realty_object.pk: 0}
            _park_percent_list.update(_park_json)
            ##
        try:
            _distance = realty_object.realty_complex.pharmacy_dist
            if _pharmacy_distance.distance > _distance:
                _percent = 100
            else:
                _percent = 100 - (_distance - _pharmacy_distance.distance) / _pharmacy_distance.distance * 100
                if _percent < 0:
                    _percent = 0
            _pharmacy_json = {realty_object.pk: _percent}
            _pharmacy_percent_list.update(_pharmacy_json)
        except DistanceMatrix.DoesNotExist:
            print('No dist for complex {} pharmacy'.format(realty_object.realty_complex.name))
            _pharmacy_json = {realty_object.pk: 0}
            _pharmacy_percent_list.update(_pharmacy_json)
            ##
        try:
            _distance = realty_object.realty_complex.nightclub_dist
            if _night_distance.distance > _distance:
                _percent = 100
            else:
                _percent = 100 - (_distance - _night_distance.distance) / _night_distance.distance * 100
                if _percent < 0:
                    _percent = 0
            _nightclub_json = {realty_object.pk: _percent}
            _nightclub_percent_list.update(_nightclub_json)
        except DistanceMatrix.DoesNotExist:
            print('No dist for complex {} park'.format(realty_object.realty_complex.name))
            _nightclub_json = {realty_object.pk: 0}
            _nightclub_percent_list.update(_nightclub_json)
            ##
        try:
            _distance = realty_object.realty_complex.market_dist
            if _market_distance.distance > _distance:
                _percent = 100
            else:
                _percent = 100 - (_distance - _market_distance.distance) / _market_distance.distance * 100
                if _percent < 0:
                    _percent = 0
            _market_json = {realty_object.pk: _percent}
            _market_percent_list.update(_market_json)
        except DistanceMatrix.DoesNotExist:
            print('No dist for complex {} market'.format(realty_object.realty_complex.name))
            _market_json = {realty_object.pk: 0}
            _market_percent_list.update(_market_json)
    _school_percent_list = _school_percent_list
    _park_percent_list = _park_percent_list
    _pharmacy_percent_list = _pharmacy_percent_list
    _nightclub_percent_list = _nightclub_percent_list
    _market_percent_list = _market_percent_list
    _final_json = dict()
    for realty_object in qs:
        _object_json = {
            realty_object.pk: {
                "school": _school_percent_list.get(realty_object.pk),
                "park": _park_percent_list.get(realty_object.pk),
                "pharmacy": _pharmacy_percent_list.get(realty_object.pk),
                "nightclub": _nightclub_percent_list.get(realty_object.pk),
                "market": _market_percent_list.get(realty_object.pk),
                "total": (int(_school_percent_list.get(realty_object.pk)) +
                          int(_park_percent_list.get(realty_object.pk)) +
                          int(_pharmacy_percent_list.get(realty_object.pk)) +
                          int(_nightclub_percent_list.get(realty_object.pk)) +
                          int(_market_percent_list.get(realty_object.pk))) / 5
            }
        }
        _final_json.update(_object_json)
    print(sorted(_final_json))
