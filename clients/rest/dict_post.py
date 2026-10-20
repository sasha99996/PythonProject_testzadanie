import requests


BASE_URL = "https://your-test-host.com"


def get_dict(
    start_date: str,
    finish_date: str,
    limit: int = 50,
    order_by: str | None = None,
    order_dir: str = "ASC",
    scope: str | None = None,
    headers: dict | None = None,
):
    url = f"{BASE_URL}/api/v1/dict"

    params = {
        "limit": limit,
        "orderDir": order_dir,
    }

    if order_by is not None:
        params["orderBy"] = order_by

    if scope is not None:
        params["scope"] = scope

    payload = {
        "start_date": start_date,
        "finish_date": finish_date,
    }

    return requests.post(
        url,
        params=params,
        json=payload,
        headers=headers,
        timeout=10,
    )