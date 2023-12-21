from sigtech.api.framework.framework_api_object import FrameworkApiObject


class Instrument(FrameworkApiObject):
    """
    Instrument class.

    This is a class for generating an object around standard instruments like cash.
    """

    def __init__(self, api_response):
        super().__init__(api_response)

    @property
    def currency(self):
        return self._get_reference_data()["currency"]
