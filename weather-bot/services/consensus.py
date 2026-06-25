def weighted_consensus(values):
    weights = {
        "ecmwf": 0.45,
        "icon-eu": 0.30,
        "gfs": 0.15,
        "arpEGE": 0.10,
    }

    result = 0
    total_w = 0

    for model, value in values.items():
        if model in weights:
            result += value * weights[model]
            total_w += weights[model]

    return result / total_w if total_w else None
