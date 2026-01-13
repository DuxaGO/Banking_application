def filter_by_state(data, state = "EXECUTED"):
    result = []
    for item in data:
        if item.get("state") == state:
            result.append(item)
    return result