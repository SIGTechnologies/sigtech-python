import logging
from typing import Any, Dict, Optional, Set, Union

from sigtech.api.client.client import Client

logger = logging.getLogger(__name__)

_GLOBAL_ENVIRONMENT = None


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
        self.object_register: Dict[str, Any] = {}
        self.all_objects: Set[Any] = set()


def env() -> Union[Environment, None]:
    """
    Retrieve the current global environment.

    :return: Returns the global Environment object.
    """
    global _GLOBAL_ENVIRONMENT
    if _GLOBAL_ENVIRONMENT is None:
        raise Exception(
            "Please initialize the environment by running the `init` method from `sigtech.api`"
        )

    return _GLOBAL_ENVIRONMENT


def init(api_client: Optional[Client] = None) -> Environment:
    """
    Initialize a global environment.
    Creates a new API session if a global environment does not already exist.

    :param api_client: API client object. (Optional) Creates a default client if not provided.
    :return: Returns the global Environment object.
    """
    global _GLOBAL_ENVIRONMENT

    if _GLOBAL_ENVIRONMENT is None:
        client = api_client or Client()

        # check API service
        logger.info(client.status.get())
        if client.status.get().status != "framework API is alive":
            raise Exception("SigTech API can not be reached. ")

        # create a new API session
        session = client.sessions.create()
        logger.info(f"Session {session.session_id} created")

        _GLOBAL_ENVIRONMENT = Environment(client, session.session_id)

    logger.info("Environment Initialized")

    return _GLOBAL_ENVIRONMENT


class obj:
    """
    A class used for handling objects.
    """

    @staticmethod
    def get(name: str) -> Optional[Any]:
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

        from sigtech.api.framework.instrument_base import Instrument

        new_instrument = Instrument(identifier=name)
        new_instrument.creation_response.wait_for_object_status()

        return new_instrument
