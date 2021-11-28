def request_contains_filter_parameter(request):
    for candidate in [
        "run_number",
        "run",
        "entries",
        "mean",
        "rms",
        "skewness",
        "kurtosis",
        "primary_dataset",
        "title",
    ]:
        for word in request.GET:
            if candidate in word:
                return True
    return False