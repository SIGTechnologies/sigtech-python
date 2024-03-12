import os

import requests


def get_session():
    try:
        token = os.environ["PLATFORM_TOKEN"]
    except KeyError:
        raise ValueError("PLATFORM_TOKEN environment variable not set")
    headers = {"Authorization": f"Bearer {token}"}
    session = requests.Session()
    session.headers.update(headers)
    return session
