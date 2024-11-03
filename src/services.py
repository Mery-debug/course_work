#Инвесткопилка
from typing import Any


#Позволяет копить через округление ваших трат.

# Можно задать комфортный порог округления: 10, 50 или 100 ₽. Траты будут округляться, и разница между фактической
# суммой трат по карте и суммой округления будет попадать на счет «Инвесткопилки».


def investment_bank(month: str, transactions: list[dict[str, Any]], limit: int) -> float:
    """Функция возвращает сумму, которую удалось бы отложить в «Инвесткопилку», шаг округления 50 р"""
    total = 0
    for transaction in transactions:
        if transaction.get("date of currency")[-9:2:-1] == month:
            if limit < 100:
                invest = transaction.get("operation").get("add") % 100
                if invest <= limit:
                    invest_t = limit - invest
                    total += invest_t
                elif invest <= 99 or invest == 00:
                    invest_t = limit * 2 - invest
                    total += invest_t
            elif limit >= 100:
                invest = transaction.get("operation").get("add") % 100
                if invest < 99 or invest == 00:
                    invest_t = limit - invest
                    total += invest_t
    return total


def simpl_search(transactions: list[dict], search_str: str) -> list[dict]:
    """Функция реализующая простой поиск по введенной пользователем строке,
    выводит список, в котором содержатся транзакции, у которых есть это слово в описании или категории"""
    total = []
    for transaction in transactions:
        if transaction.get("description") == search_str or transaction.get("category") == search_str:
            total.append(transaction)
    return total


