def step_to_int(step: int|str) -> int:

    if isinstance(step, int):
        return int(step)
    elif isinstance(step, str) and str(step) == "koniec":
        return -1
    else:
        raise ValueError(f"Cannot convert value {step}!")
    
def step_to_selection_index(step: int, max_step: int) -> int:

    if step == -1:
        return max_step
    else:
        return step