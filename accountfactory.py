from typing import Optional
from account import Account, DepositAccount, DebitAccount, CreditAccount
from plan import Plan, DepositPlan, CreditPlan

class AccountFactory:
    '''Factory (Factory method) class for creating Account instances.'''

    @staticmethod
    def create(owner: int, plan: Plan) -> Account:
        if isinstance(plan, DepositPlan):
            return DepositAccount(owner, plan.id)
        elif isinstance(plan, CreditPlan):
            return CreditAccount(owner, plan.id)
        else:
            return DebitAccount(owner, plan.id)