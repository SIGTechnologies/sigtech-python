import os
from typing import Optional, Type


class ClientSettings:
    """
    Singleton class to handle the settings of a REST API Client.
    It provides SIGTECH API settings, including API URL, API key, wait timeout and timer view toggle.
    """

    SIGTECH_API_URL: Optional[str] = None
    SIGTECH_API_KEY: Optional[str] = None
    SIGTECH_API_WAIT_TIMEOUT: Optional[int] = None
    SIGTECH_API_WAIT_TIMER: Optional[bool] = None

    _instance: Optional['ClientSettings'] = None

    def __new__(cls: Type['ClientSettings']) -> 'ClientSettings':
        """
        Create a new instance of the class if one doesn't exist already.
        The API settings are initialized here if they were not set before.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Only initialize class variables if they were not set before
            cls.SIGTECH_API_URL = cls.SIGTECH_API_URL or os.environ.get('SIGTECH_API_URL',
                                                                        'api.framework.prod.sigtech.com')
            cls.SIGTECH_API_KEY = cls.SIGTECH_API_KEY or os.environ.get('SIGTECH_API_KEY', '')
            cls.SIGTECH_API_WAIT_TIMEOUT = cls.SIGTECH_API_WAIT_TIMEOUT or int(
                os.environ.get('SIGTECH_API_WAIT_TIMEOUT', 60))
            if cls.SIGTECH_API_WAIT_TIMER is None:
                cls.SIGTECH_API_WAIT_TIMER = os.environ.get('SIGTECH_API_WAIT_TIMER', 'true').lower() == 'true'

        return cls._instance

    @classmethod
    def clear(cls):
        """ Clear singleton"""
        cls._instance = None
        cls.SIGTECH_API_URL = None
        cls.SIGTECH_API_KEY = None
        cls.SIGTECH_API_WAIT_TIMEOUT = None
        cls.SIGTECH_API_WAIT_TIMER = None
