from typing import List
from dataoperator import DataOperator

current_time: int = 0
update_queue: List[int] = []

class TimeKeeper:
    '''Модуль, считающий дни и
    катализирующий обновление счетов по их тарифам.'''

    def add(self, account: int):
        update_queue.append(account)

    def current_time(self):
        ct = current_time
        return ct

    def increase(self):
        for account in update_queue:
            DataOperator().get(account, "Account").update()
        global current_time
        current_time += 1

    def get(self) -> int:
        global current_time
        return current_time