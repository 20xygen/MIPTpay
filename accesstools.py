similar_names = [["Account", "DebitAccount", "DepositAccount", "CreditAccount"],
                 ["Plan", "DebitPlan", "DepositPlan", "CreditPlan"]]

gods = ["DataOperator", "Admin"]

def available_from(me, *valid: str):
    # t = dir(me.f_back.f_locals)
    # try:
    #     k = me.f_back.f_locals
    #     r = me.f_back.f_locals['__class__']
    # except Exception:
    #     pass
    dep = me.f_back.f_locals["self"].__class__.__qualname__
    self = me.f_locals["self"].__class__.__qualname__
    with_similar = []
    for i in valid:
        flag = False
        for j in similar_names:
            if i in j:
                flag = True
                with_similar += j
                # with_similar.append(*j)
        if not flag:
            with_similar.append(i)
    flag = False
    for j in similar_names:
        if self in j:
            flag = True
            with_similar += j
            # with_similar.append(*j)
    if not flag:
        with_similar.append(self)
    if dep not in with_similar:
        raise TypeError(dep + " is not " + ', or '.join(with_similar))
