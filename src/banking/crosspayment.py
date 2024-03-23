import src


""" The module executing the singleton pattern for the class CrossPaymentSystem. """

def get_cpf():
    if src.system is None:
        src.system = src.CrossPaymentSystem()
    return src.system