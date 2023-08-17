import logging
from typing import TYPE_CHECKING, Dict, Optional, Set

from sigtech.api.client.client import Client
from sigtech.api.client.utils import SigApiException

if TYPE_CHECKING:
    # Used at import time only, because of circular dependency
    from sigtech.api.framework.framework_api_object import FrameworkApiObject

logger = logging.getLogger(__name__)

_GLOBAL_ENVIRONMENT: Optional["Environment"] = None


class Environment:
    """
    Class to hold the environments data
    """

    def __init__(self, client: Client, session_id: str) -> None:
        """
        Initialize an environment with given client and session id.

        :param client: Client object
        :param session_id: String representing session id
        """
        self.session_id = session_id
        self.client = client
        self.object_register: Dict[str, "FrameworkApiObject"] = {}
        self.all_objects: Set["FrameworkApiObject"] = set()


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

    # create a new API session
    session = client.sessions.create()
    logger.info(f"Session {session.session_id} created")

    return Environment(client, session.session_id)


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
