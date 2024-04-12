from typing import List
from datetime import datetime
import src

from dateutil import parser

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

    def update(self):
        dm = __import__("src.miptpaydj.mainapp.models").DiaryModel
        am = __import__("src.miptpaydj.mainapp.models").AccountModel
        diary = dm.objects.get(parameter="Date")
        print(diary.value)
        dt = parser.parse(str(diary.value))
        print(dt)
        print(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
        print(datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second))
        delta = datetime.now() - datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
        delta = delta.days * 24 + delta.seconds // 3600
        print("Delta is", delta)
        for account_ in am.objects.all():
            account = src.DataOperator().get(account_.id, "Account")
            for i in range(delta):
                account.update()
            src.DataOperator().done_with(account_.id, "Account")
        diary.value = datetime.now()
        diary.save()
