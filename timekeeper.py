from typing import List
import dataoperator


'''Модуль, считающий дни и
катализирующий обновление счетов по их тарифам.'''


current_time: int = 0
update_queue: List[int] = []

def add(account: int):
    update_queue.append(account)

def increase():
    for account in update_queue:
        dataoperator.get(account, "Account").update()
    global current_time
    current_time += 1

def get() -> int:
    global current_time
    return current_time