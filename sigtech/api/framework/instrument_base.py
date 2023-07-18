from sigtech.api.framework.environment import env
from sigtech.api.framework.framework_api_object import FrameworkApiObject


class Instrument(FrameworkApiObject):
    """
    Instrument class.

    This is a class for generating an object around standard instruments like cash.
    """

    def __init__(self, identifier: str):
        api_response = self._get_instrument_obj(env().session_id, identifier=identifier)
        super().__init__(api_response)

    def _get_instrument_obj(self, session_id: str, identifier: str):
        """
        Fetch instrument from API.
        """

        return env().client.instruments.create(
            session_id=session_id,
            identifier=identifier,
        )
