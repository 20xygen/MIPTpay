from transaction import Transaction
from typing import Optional


class CrossPaymentSystem:
    def transfer(self, dep_bank: int, departure: int, dest_bank: int, destination: int, sender: int,
                 amount: float) -> bool:
        from dataoperator import DataOperator
        dep_bank_obj = DataOperator().get(dep_bank, "Bank")
        dest_bank_obj = DataOperator().get(dest_bank, "Bank")
        if not dep_bank_obj.valid_client(departure, sender):
            return False
        trans = Transaction(departure, destination, amount)
        DataOperator().put(trans)
        if dep_bank_obj.put_offer(departure, amount) and dest_bank_obj.put_offer(destination, amount):
            dep_bank_obj.do_get(departure, amount)
            dest_bank_obj.do_put(destination, amount)
            trans.prove()
            return True
        else:
            trans.cancel()
            return False


system: Optional[CrossPaymentSystem] = None