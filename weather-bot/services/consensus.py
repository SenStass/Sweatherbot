def weighted_consensus(values):
    weights = {
        "ecmwf": 0.45,
        "icon": 0.35,
        "gfs": 0.20,
        "slav": 0.25,
        "wrf": 0.15
    }

    result = 0
    total_w = 0

    for model, value in values.items():
        if model in weights:
            result += value * weights[model]
            total_w += weights[model]

    return result / total_w if total_w else None
