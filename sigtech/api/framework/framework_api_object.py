from sigtech.api.framework.environment import env

class FrameworkApiObject:

    def __init__(self, entity):
        self.entity = entity
        self._status = None
        self._name = None
        env().all_objects.add(self)

    @property
    def api_status(self):
        if self._status != 'SUCCEEDED':
            entity = self.entity.latest_object_response()
            self._status = entity.status
        return self._status

    @property
    def api_object_id(self):
        return self.entity.object_id

    @property
    def api_session_id(self):
        return self.entity.session_id

    @property
    def name(self):
        if self._name is not None:
            return self._name

        entity = self.entity.wait_for_object_status(property_name="name")
        self._name = entity.name
        env().object_register[self._name] = self
        return self._name

