import crosspaymentsystem

def get():
    if crosspaymentsystem.system is None:
        crosspaymentsystem.system = crosspaymentsystem.CrossPaymentSystem()
    return crosspaymentsystem.system