current_time: int = 0
global current_time

def increase():
    current_time += 1

def get() -> int:
    return current_time