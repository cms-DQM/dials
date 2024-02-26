def preprocessing_filter_spec(endpoints):
    filtered = []
    for path, path_regex, method, callback in endpoints:
        if path == "/api/v1/schema":
            continue
        filtered.append((path, path_regex, method, callback))
    return filtered
