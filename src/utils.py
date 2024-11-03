import datetime
import os.path
import pandas as pd
import os
from typing import Any, Union

import requests
from dotenv import load_dotenv
from pandas import DataFrame


def hello_date():
    """Функция приветствия от времени суток"""
    now = datetime.datetime.now()
    now += datetime.timedelta()
    hello = {"hello": ""}
    if 4 < now.hour <= 12:
        hello["hello"] = 'Доброе утро'
    if 16 >= now.hour > 12:
        hello["hello"] = 'Добрый день'
    if 24 >= now.hour > 16:
        hello["hello"] = 'Добрый вечер'
    if 4 >= now.hour >= 0:
        hello["hello"] = 'Доброй ночи'

    return hello


path_xlsx = "../../data/operations.xlsx"


def read_file(path: str) -> list[dict]:
    """Функция чтения excel файла"""
    file_name = os.path.join(os.path.abspath(__name__), path)
    transactions = []
    transaction = pd.read_excel(file_name)
    for index, row in transaction.iterrows():
        transactions.append(
            {
                "date of operation": row["Дата операции"],
                "date of currency": row["Дата платежа"],
                "card number": row["Номер карты"],
                "status": row["Статус"],
                "operation": {
                    "add": row["Сумма операции"],
                    "currency": row["Валюта операции"]
                },
                "add": row["Сумма платежа"],
                "currency": row["Валюта платежа"],
                "cashback": row["Кэшбэк"],
                "category": row["Категория"],
                "description": row["Описание"],
                "Investment bank": row["Округление на инвесткопилку"],
                "add with round": row["Сумма операции с округлением"]
            })
    transactions.pop(1)
    return transactions


print(read_file(path_xlsx))


def return_cash() -> Union[list, str]:
    """Function API take dict transaction and return amount"""
    load_dotenv()
    api_key = os.getenv("API_KEY")
    url_usd = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=1"
    url_eur = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=EUR&amount=1"
    headers = {"apikey": f"{api_key}"}
    response_usd = requests.get(url_usd, headers=headers)
    response_eur = requests.get(url_eur, headers=headers)
    if response_usd.status_code == 200 and response_eur.status_code == 200:
        eur = round(response_eur.json()["result"], 2)
        usd = round(response_usd.json()["result"], 2)
        return [eur, usd]
    else:
        return f"Возможные причины {response_eur.reason} {response_usd.reason}"


def return_invest() -> list[dict]:
    """
    Функция АПИ которая выводит акции из s&p 500 по запросу пользователя,
    ввести в качестве аргумента название акции, например APPL
    """
    load_dotenv()
    response = []
    apikey = os.getenv("APIKEY")
    url = f"https://financialmodelingprep.com/api/v3/quote/AAPL,AMZN,GOOGL,MSFT,TSLA?apikey={apikey}"
    response.append(requests.get(url).json())
    return response


# print(return_invest())


def card_info(transactions: list[dict]) -> list:
    total_card = 0
    total_card_2 = 0
    total_card_3 = 0
    card = ""
    card_2 = ""
    card_3 = ""
    for transaction in transactions:
        card = transaction.get("card number")
        if card:
            total_card += transaction.get("operation").get("add")
        # elif card_2:
        #     total_card_2 = sum(transaction.get("operation").get("add"))
        # elif card_3:
        #     total_card_3 = sum(transaction.get("operation").get("add"))
    total_cash = total_card / 100
    # total_cash_2 = total_card_2 / 100
    # total_cash_3 = total_card_3 / 100
    return [card, round(total_card, 2), round(total_cash, 2)]


# print(card_info(read_file(path)))


# def top_5(transactions: list[dict]) ->:
#     for transaction in transactions:
#         df = pd.DataFrame()
