import os
import pytest
from sigtech.api.client.settings import ClientSettings


class TestClientSettings:

    @pytest.fixture(autouse=True)
    def setup_class(self):
        # Resetting the singleton instance before each test
        ClientSettings.clear()
        # Clearing environment variables
        os.environ.pop('SIGTECH_API_URL', None)
        os.environ.pop('SIGTECH_API_KEY', None)
        os.environ.pop('SIGTECH_API_WAIT_TIMEOUT', None)
        os.environ.pop('SIGTECH_API_WAIT_TIMER', None)

    def test_singleton(self):
        settings1 = ClientSettings()
        settings2 = ClientSettings()
        assert settings1 is settings2, "Singleton instances are not the same!"

    def test_default_values(self):
        settings = ClientSettings()
        assert settings.SIGTECH_API_URL == 'api.framework.prod.sigtech.com'
        assert settings.SIGTECH_API_KEY == ''
        assert settings.SIGTECH_API_WAIT_TIMEOUT == 60
        assert settings.SIGTECH_API_WAIT_TIMER is True

    def test_environment_variables(self):
        os.environ['SIGTECH_API_URL'] = 'test_url'
        os.environ['SIGTECH_API_KEY'] = 'test_key'
        os.environ['SIGTECH_API_WAIT_TIMEOUT'] = '30'
        os.environ['SIGTECH_API_WAIT_TIMER'] = 'false'
        settings = ClientSettings()
        assert settings.SIGTECH_API_URL == 'test_url'
        assert settings.SIGTECH_API_KEY == 'test_key'
        assert settings.SIGTECH_API_WAIT_TIMEOUT == 30
        assert settings.SIGTECH_API_WAIT_TIMER is False

    def test_class_variable_setting(self):
        ClientSettings.SIGTECH_API_URL = 'set_url'
        ClientSettings.SIGTECH_API_KEY = 'set_key'
        ClientSettings.SIGTECH_API_WAIT_TIMEOUT = 120
        ClientSettings.SIGTECH_API_WAIT_TIMER = False
        settings = ClientSettings()
        assert settings.SIGTECH_API_URL == 'set_url'
        assert settings.SIGTECH_API_KEY == 'set_key'
        assert settings.SIGTECH_API_WAIT_TIMEOUT == 120
        assert settings.SIGTECH_API_WAIT_TIMER is False
