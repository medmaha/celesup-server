def get_query_params(url: str) -> dict[str, str]:
    data = {}
    try:
        query_string = url.split("?")[1]
        queries = query_string.split("&")

        for query in queries:
            key, value = query.split("=")
            if key and value:
                data[key] = value

        return data
    except:
        return data
