import datetime
import os.path
import pandas as pd
import os
from typing import Any, Union

import requests
from dotenv import load_dotenv


def hello_date():
    now = datetime.datetime.now()
    now += datetime.timedelta()
    hello = 0
    if 4 < now.hour <= 12:
        hello = 'Доброе утро'
    if 16 >= now.hour > 12:
        hello = 'Добрый день'
    if 24 >= now.hour > 16:
        hello = 'Добрый вечер'
    if 4 >= now.hour >= 0:
        hello = 'Доброй ночи'

    return hello


def read_file(path: str) -> list[dict]:
    file_name = os.path.join(os.path.abspath(__name__), path)
    """function which read xlsx files with lib pandas"""
    transactions = []
    transaction = pd.read_excel(file_name)
    for index, row in transaction.iterrows():
        transactions.append(
            {
                "date of operation": str(row["Дата операции"]),
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
                "MCC": row["MCC"],
                "description": row["Описание"],
                "bonuses": row["Бонусы"],
                "Investment bank": row["Округление на инвесткопилку"],
                "add with round": row["Сумма операции с округлением"]
            })
    return transactions


def return_cash(amount: Union[int, str], from_currency: str, to_currency: str) -> Any:
    """Function API take dict transaction and return amount in RUB only"""
    load_dotenv()
    api_key = os.getenv("API_KEY")
    url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_currency}&from={from_currency}&amount={amount}"
    headers = {"apikey": f"{api_key}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        if from_currency in ["EUR", "USD"]:
            return round(response.json()["result"], 2)
        else:
            return amount
    else:
        return f"Возможная причина {response.reason}"


def return_invest(data: str) -> list[dict]:
    # url = f"http://api.marketstack.com/v1/eod/{data}"
    # url_2 = f"http://api.marketstack.com/v1/eod/latest"
    load_dotenv()
    apikey = os.getenv("APIKEY")
    url = f"https://api.marketstack.com/v1/eod?access_key={apikey}"
    querystring = {"symbols": "AAPL"}
    response = requests.get(url, params=querystring)

    print(response.json())
def card_info(transactions: list[dict], card_number: str) -> list[dict]:
    pass


def sort_by_sum(transaction: list[dict]) -> list[dict]:
    pass
