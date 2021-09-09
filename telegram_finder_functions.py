from bs4 import BeautifulSoup
import pandas as pd
import random
import re
import requests
import time

def get(query, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param query: запрос с адресом
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    delay = 0
    for i in range(max_retries):
        try:
            response = requests.get(query)
            return response.json()
        except:
            pass
        time.sleep(delay)
        delay = min(delay * backoff_factor, timeout)
        delay += random.random()
    return response

def trim_link(link):
    if link[-1] == '/':
        link = link[:-1]
    name = link[link.rfind("/")+1:]
    return name

def trim_email(email):
    name = email[:email.rfind("@")]
    return name

def test_telegram(nick):
    query = 'https://telegram.me/' + nick
    response = get(query)
    soup = BeautifulSoup(response.text, 'html.parser')
    name = soup.find("div", class_="tgme_page_title")
    if name:
        print(name.text, '-', query)
    else:
        print(nick, '- такого аккаунта нет')

def permutator(name):
    name_list = [name]
    has_numbers = any(c.isdigit() for c in name)
    # remove punctuation
    table = str.maketrans('','','.-_')
    name_list.append(name.translate(table))
    if has_numbers:
        # remove numbers
        table = str.maketrans('','','0123456789')
        name_list.append(name.translate(table))
        # remove punctuation and numbers
        table = str.maketrans('','','.-_0123456789')
        name_list.append(name.translate(table))
    if name.find('-') > 0:
        # replace dashes with underscores
        table = str.maketrans('-','_')
        name_list.append(name.translate(table))
        # replace dashes with dots
        table = str.maketrans('-','.')
        name_list.append(name.translate(table))
        if has_numbers:
            # replace dashes with underscores, remove numbers
            table = str.maketrans('-','_','0123456789')
            name_list.append(name.translate(table))
            # replace dashes with dots, remove numbers
            table = str.maketrans('-','.','0123456789')
            name_list.append(name.translate(table))
    if name.find('.') > 0:
        # replace dots with underscores
        table = str.maketrans('.','_')
        name_list.append(name.translate(table))
        # replace dots with dashes
        table = str.maketrans('.','-')
        name_list.append(name.translate(table))
        if has_numbers:
            # replace dots with underscores, remove numbers
            table = str.maketrans('.','_','0123456789')
            name_list.append(name.translate(table))
            # replace dots with dashes, remove numbers
            table = str.maketrans('.','-','0123456789')
            name_list.append(name.translate(table))
    if name.find('_') > 0:
        # replace underscores with dots
        table = str.maketrans('_','.')
        name_list.append(name.translate(table))
        # replace underscores with dashes
        table = str.maketrans('_','-')
        name_list.append(name.translate(table))
        if has_numbers:
            # replace underscores with dots, remove numbers
            table = str.maketrans('_','.','0123456789')
            name_list.append(name.translate(table))
            # replace underscores with dashes, remove numbers
            table = str.maketrans('_','-','0123456789')
            name_list.append(name.translate(table))
    return name_list