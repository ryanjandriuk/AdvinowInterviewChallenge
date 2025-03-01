def str_is_true(s: str):
    s_clean = s.replace(" ", "").lower()
    return s_clean == "true" or s_clean == "yes"

def str_is_false(s: str):
    s_clean = s.replace(" ", "").lower()
    return s_clean == "false" or s_clean == "no"

def str_to_bool(s: str):
    if str_is_true(s):
        return True
    elif str_is_false(s):
        return False
    raise ValueError(f"Given string {s} does not contain a recognized boolean!")