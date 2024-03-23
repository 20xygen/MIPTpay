import src

class AccountFactory:
    """ Factory (Factory method) class for creating Account instances. """

    @staticmethod
    def create(owner: int, plan: src.Plan) -> src.Account:
        if isinstance(plan, src.DepositPlan):
            return src.DepositAccount(owner, plan.id)
        elif isinstance(plan, src.CreditPlan):
            return src.CreditAccount(owner, plan.id)
        else:
            return src.DebitAccount(owner, plan.id)