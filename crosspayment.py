import crosspaymentsystem

""" The module executing the singleton pattern for the class CrossPaymentSystem. """

def get():
    if crosspaymentsystem.system is None:
        crosspaymentsystem.system = crosspaymentsystem.CrossPaymentSystem()
    return crosspaymentsystem.system