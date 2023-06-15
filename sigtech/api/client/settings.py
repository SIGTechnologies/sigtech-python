import os


class ClientSettings:
    SIGTECH_API_URL = None
    SIGTECH_API_KEY = None
    SIGTECH_API_WAIT_TIMEOUT = None
    SIGTECH_API_WAIT_TIMER = None

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        cls.SIGTECH_API_URL = cls.SIGTECH_API_URL or os.environ.get('SIGTECH_API_URL',
                                                                    'api.framework.prod.sigtech.com')
        cls.SIGTECH_API_KEY = cls.SIGTECH_API_KEY or os.environ.get('SIGTECH_API_KEY', '')
        cls.SIGTECH_API_WAIT_TIMEOUT = cls.SIGTECH_API_WAIT_TIMEOUT or os.environ.get('SIGTECH_API_WAIT_TIMEOUT', 60)
        cls.SIGTECH_API_WAIT_TIMER = cls.SIGTECH_API_WAIT_TIMER or os.environ.get('SIGTECH_API_WAIT_TIMER', 'true').lower() == 'true'

        return cls._instance
