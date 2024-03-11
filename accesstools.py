def available_from(me, *valid: str):
    dep = me.f_back.f_locals["self"].__class__.__qualname__
    self = me.f_locals["self"].__class__.__qualname__
    if dep not in valid and self != dep:
        raise TypeError(dep + " is not " + self + " or " + ' / '.join(valid))
