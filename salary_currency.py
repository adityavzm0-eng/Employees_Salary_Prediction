def format_indian_number(amount: float) -> str:
    whole_number = str(int(round(amount)))
    if len(whole_number) <= 3:
        return whole_number

    last_group = whole_number[-3:]
    remaining = whole_number[:-3]
    groups = []
    while remaining:
        groups.append(remaining[-2:])
        remaining = remaining[:-2]
    return f"{','.join(reversed(groups))},{last_group}"