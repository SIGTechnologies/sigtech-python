from sigtech.api.framework.framework_api_object import FrameworkApiObject


class Index(FrameworkApiObject):
    @property
    def currency(self):
        return self._get_reference_data()["currency"]

    @property
    def description(self):
        return self._get_reference_data()["description"]
