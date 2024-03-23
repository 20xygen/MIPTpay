import src


class PlanFactory:
    @staticmethod
    def create_debit_plan(transfer_limit: src.TransferLimit):
        return src.DebitPlan(transfer_limit.transfer_limit, transfer_limit.decreased_transfer_limit)

    @staticmethod
    def create_deposit_plan(transfer_limit: src.TransferLimit,
                            period: src.Period, commission: src.Commission):
        return src.DepositPlan(period.period, period.decreased_period,
                         commission.commission, commission.increased_commission,
                         transfer_limit.transfer_limit, transfer_limit.decreased_transfer_limit)

    @staticmethod
    def create_credit_plan(transfer_limit: src.TransferLimit,
                            lower_limit: src.LowerLimit, commission: src.Commission):
        return src.CreditPlan(lower_limit.lower_limit, lower_limit.decreased_lower_limit,
                         commission.commission, commission.increased_commission,
                         transfer_limit.transfer_limit, transfer_limit.decreased_transfer_limit)
