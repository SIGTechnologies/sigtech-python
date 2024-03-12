import os

import requests


def get_session():
    try:
        token = os.environ["SIGTECH_PLATFORM_TOKEN"]
    except KeyError:
        raise ValueError("SIGTECH_PLATFORM_TOKEN environment variable not set")
    headers = {"Authorization": f"Bearer {token}"}
    session = requests.Session()
    session.headers.update(headers)
    return session
