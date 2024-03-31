from typing import List
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
        global current_time
        current_time += 1

    def get(self) -> int:
        global current_time
        return current_time