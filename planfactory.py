from plan import DebitPlan, DepositPlan, CreditPlan
from typing import Optional

class PlanProperty:
    pass

class Commission(PlanProperty):
    commission: float
    increased_commission: float

    def __init__(self, commission: float, increased_commission: Optional[float] = None):
        self.commission = commission
        if increased_commission is not None:
            self.increased_commission = increased_commission
        else:
            self.increased_commission = commission

class Period(PlanProperty):
    period: int
    decreased_period: int

    def __init__(self, period: int, decreased_period: Optional[int] = None):
        self.period = period
        if decreased_period is not None:
            self.decreased_period = decreased_period
        else:
            self.decreased_period = period

class LowerLimit(PlanProperty):
    lower_limit: float
    decreased_lower_limit: float

    def __init__(self, lower_limit: float, decreased_lower_limit: Optional[float] = None):
        self.lower_limit = lower_limit
        if decreased_lower_limit is not None:
            self.decreased_lower_limit = decreased_lower_limit
        else:
            self.decreased_lower_limit = lower_limit

class UpperLimit(PlanProperty):
    upper_limit: float
    decreased_upper_limit: float

    def __init__(self, upper_limit: float, decreased_upper_limit: Optional[float] = None):
        self.upper_limit = upper_limit
        if decreased_upper_limit is not None:
            self.decreased_upper_limit = decreased_upper_limit
        else:
            self.decreased_upper_limit = upper_limit

class TransferLimit(PlanProperty):
    transfer_limit: float
    decreased_transfer_limit: float

    def __init__(self, transfer_limit: float, decreased_transfer_limit: Optional[float] = None):
        self.transfer_limit = transfer_limit
        if decreased_transfer_limit is not None:
            self.decreased_transfer_limit = decreased_transfer_limit
        else:
            self.decreased_transfer_limit = transfer_limit

class PlanFactory:
    @staticmethod
    def create_debit_plan(transfer_limit: TransferLimit):
        return DebitPlan(transfer_limit.transfer_limit, transfer_limit.decreased_transfer_limit)

    @staticmethod
    def create_deposit_plan(transfer_limit: TransferLimit,
                            period: Period, commission: Commission):
        return DepositPlan(period.period, period.decreased_period,
                         commission.commission, commission.increased_commission,
                         transfer_limit.transfer_limit, transfer_limit.decreased_transfer_limit)

    @staticmethod
    def create_credit_plan(transfer_limit: TransferLimit,
                            lower_limit: LowerLimit, commission: Commission):
        return CreditPlan(lower_limit.lower_limit, lower_limit.decreased_lower_limit,
                         commission.commission, commission.increased_commission,
                         transfer_limit.transfer_limit, transfer_limit.decreased_transfer_limit)
