import src

class PlanCategory:
    name: str
    commission: bool
    period: bool
    lower_limit: bool
    upper_limit: bool
    transfer_limit: bool

    def _init__(self, name: str, commission: bool, period: bool, lower_limit: bool, upper_limit: bool, transfer_limit: bool):
        self.name = name
        self.commission = commission
        self.period = period
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.transfer_limit = transfer_limit

    def construct(self, *args):
        output = []
        pin = 0
        # needed?
