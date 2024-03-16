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

    def info(self) -> str:
        ans = f"Комиссия, начисляемая или взымаемая бынком: {self.commission}\n"
        ans += f"(Комиссия при ненадежном аккаунте: {self.increased_commission})"
        return ans

class Period(PlanProperty):
    period: int
    decreased_period: int

    def __init__(self, period: int, decreased_period: Optional[int] = None):
        self.period = period
        if decreased_period is not None:
            self.decreased_period = decreased_period
        else:
            self.decreased_period = period

    def info(self) -> str:
        ans = f"Срок вклада: {self.period}\n"
        ans += f"(Срок при ненадежном аккаунте: {self.decreased_period})"
        return ans

class LowerLimit(PlanProperty):
    lower_limit: float
    decreased_lower_limit: float

    def __init__(self, lower_limit: float, decreased_lower_limit: Optional[float] = None):
        self.lower_limit = lower_limit
        if decreased_lower_limit is not None:
            self.decreased_lower_limit = decreased_lower_limit
        else:
            self.decreased_lower_limit = lower_limit

    def info(self) -> str:
        ans = f"Минимальный остаток: {self.lower_limit}\n"
        ans += f"(Минимальный остаток при ненадежном аккаунте: {self.decreased_lower_limit})"
        return ans

class UpperLimit(PlanProperty):
    upper_limit: float
    decreased_upper_limit: float

    def __init__(self, upper_limit: float, decreased_upper_limit: Optional[float] = None):
        self.upper_limit = upper_limit
        if decreased_upper_limit is not None:
            self.decreased_upper_limit = decreased_upper_limit
        else:
            self.decreased_upper_limit = upper_limit

    def info(self) -> str:
        ans = f"Максимальный балланс: {self.upper_limit}\n"
        ans += f"(Максимальный балланс при ненадежном аккаунте: {self.decreased_upper_limit})"
        return ans

class TransferLimit(PlanProperty):
    transfer_limit: float
    decreased_transfer_limit: float

    def __init__(self, transfer_limit: float, decreased_transfer_limit: Optional[float] = None):
        self.transfer_limit = transfer_limit
        if decreased_transfer_limit is not None:
            self.decreased_transfer_limit = decreased_transfer_limit
        else:
            self.decreased_transfer_limit = transfer_limit

    def info(self) -> str:
        ans = f"Лимит на переводы: {self.transfer_limit}\n"
        ans += f"(Лимит на переводы при ненадежном аккаунте: {self.decreased_transfer_limit})"
        return ans

class PlanFactory:
    @staticmethod
    def create_debit_plan(transfer_limit: TransferLimit):
        from plan import DebitPlan
        return DebitPlan(transfer_limit.transfer_limit, transfer_limit.decreased_transfer_limit)

    @staticmethod
    def create_deposit_plan(transfer_limit: TransferLimit,
                            period: Period, commission: Commission):
        from plan import DepositPlan
        return DepositPlan(period.period, period.decreased_period,
                         commission.commission, commission.increased_commission,
                         transfer_limit.transfer_limit, transfer_limit.decreased_transfer_limit)

    @staticmethod
    def create_credit_plan(transfer_limit: TransferLimit,
                            lower_limit: LowerLimit, commission: Commission):
        from plan import CreditPlan
        return CreditPlan(lower_limit.lower_limit, lower_limit.decreased_lower_limit,
                         commission.commission, commission.increased_commission,
                         transfer_limit.transfer_limit, transfer_limit.decreased_transfer_limit)
