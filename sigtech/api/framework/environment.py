import logging
from typing import TYPE_CHECKING, Any, Dict, Optional, Set

from sigtech.api.client.client import Client
from sigtech.api.client.utils import SigApiException
from sigtech.api.framework import config

if TYPE_CHECKING:
    # Used at import time only, because of circular dependency
    from sigtech.api.framework.framework_api_object import FrameworkApiObject

logger = logging.getLogger(__name__)

_GLOBAL_ENVIRONMENT: Optional["Environment"] = None


class Environment:
    """
    Class to hold the environments data
    """

    def __init__(self, client: Client) -> None:
        """
        Initialize an environment with given client and session id.

        :param client: Client object
        :param session_id: String representing session id
        """
        self._session_id = None
        self.client = client
        self.object_register: Dict[str, "FrameworkApiObject"] = {}
        self.all_objects: Set["FrameworkApiObject"] = set()
        self.config: Dict[str, Any] = {}

    def __getitem__(self, key: str) -> "FrameworkApiObject":
        return self.config[key]

    def __setitem__(self, key: str, value: Any):
        if self._session_id is not None:
            raise SigApiException("Cannot change environment config after using it.")
        self.config[key] = value

    @property
    def session_id(self):
        if self._session_id is not None:
            return self._session_id
        empty = object()
        settings = {}

        v = self.config.get(config.DISABLE_T_COST_NETTING, empty)
        if v is not empty:
            settings["transactionCostNetting"] = _invert(v)

        v = self.config.get(config.IGNORE_T_COSTS, empty)
        if v is not empty:
            settings["transactionCosts"] = _invert(v)

        v = self.config.get(config.TM_TIMEZONE, empty)
        if v is not empty:
            settings["timezone"] = v

        v = self.config.get(config.EXCESS_RETURN_ONLY, empty)
        if v is not empty:
            settings["totalReturn"] = _invert(v)

        session = self.client.sessions.create(settings=settings)
        self._session_id = session.session_id
        logger.info(f"Session {session.session_id} created")
        return self._session_id


def env() -> Environment:
    """
    Retrieve the current global environment.

    :return: Returns the global Environment object.
    """
    if _GLOBAL_ENVIRONMENT is None:
        raise SigApiException(
            "Please initialize the environment by running the `init` method from"
            " `sigtech.api`"
        )

    return _GLOBAL_ENVIRONMENT


def init(api_client: Optional[Client] = None) -> Environment:
    """
    Initialize a global environment. Creates a new API session if a global
    environment does not already exist.

    :param api_client: API client object. (Optional) Creates a default client if
        not provided.
    :return: Returns the global Environment object.
    """

    global _GLOBAL_ENVIRONMENT
    _GLOBAL_ENVIRONMENT = _GLOBAL_ENVIRONMENT or _initialise_environment(api_client)
    logger.info("Environment Initialized")
    return _GLOBAL_ENVIRONMENT


def _initialise_environment(api_client) -> Environment:
    client = api_client or Client()

    # check API service
    logger.info(client.status.get())
    if client.status.get().status != "framework API is alive":
        raise SigApiException("SigTech API can not be reached.")

    return Environment(client)


class obj:
    """
    A class used for handling objects.
    """

    @staticmethod
    def get(name: str) -> "FrameworkApiObject":
        """
        Retrieve the object using the framework name from the environment.

        :param name: The name of the object.
        :return: The object if it exists, else None.
        """

        # Retrieve the current environment
        current_env = env()
        if name in current_env.object_register:
            return current_env.object_register[name]

        for fa_obj in current_env.all_objects:
            if name == fa_obj.name:
                return fa_obj

            if name == fa_obj.api_object_id:
                return fa_obj

        # pylint: disable=import-outside-toplevel
        from sigtech.api.framework.instrument_base import Instrument

        new_instrument = Instrument(identifier=name)
        new_instrument.creation_response.wait_for_object_status()

        return new_instrument


def _invert(b: Optional[bool]):
    if b is None:
        return None
    return not b
