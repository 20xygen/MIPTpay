from typing import List
from datetime import datetime
import src

current_time: int = 0
update_queue: List[int] = []

class TimeKeeper:  # TODO: make singleton.
    """ A class that counts the days and
    catalyzes the updating of accounts according to their tariffs. """

    def add(self, account: int):
        update_queue.append(account)

    def current_time(self):
        ct = current_time
        return ct

    def increase(self):
        for account in update_queue:
            src.DataOperator().get(account, "Account").update()
            src.DataOperator().done_with(account, "Account")
        global current_time
        current_time += 1

    def get(self) -> int:
        global current_time
        return current_time

    def is_leap(self, year: int) -> bool:
        return year % 4 == 0 and year % 100 != 0 or year % 400 == 0

    def date_to_hours(self, date: datetime) -> int:
        res = 3
        for i in range(1, date.year):
            if self.is_leap(i):
                res += 366 * 24
            else:
                res += 365 * 24
        days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if self.is_leap(date.year):
            days[1] = 29
        for i in range(date.month - 1):
            res += days[i] * 24
        res += (date.day - 1) * 24
        res += date.hour
        return res

    def from_inception(self, date: datetime) -> int:
        return self.date_to_hours(date) - self.date_to_hours(datetime(2024, 4, 1, 0, 0, 0))

    def update(self):
        diary = src.DiaryModel.objects.get(parameter="Date")
        delta = self.from_inception(datetime.now()) - self.from_inception(diary.value)
        for account_ in Account.objects.all():
            account = src.DataOperator().get(account_.id, "Account")
            account.update(delta)
            src.DataOperator().done_with(account_.id, "Account")
