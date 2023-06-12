from sigtech.API.SigApi import FrameworkApi


class Environment:
    GLOBAL_SESSION = None
    API = FrameworkApi()


def init():

    # check service
    print(Environment.API.status.get())

    if Environment.GLOBAL_SESSION is None:
        # if new init or _GLOBAL_SESSION is None
        session = Environment.API.sessions.create()

        # check status

        #
        Environment.GLOBAL_SESSION = session.session_id

    return Environment


def _request_object(api_response):
    # check response

    return FrameworkApiObject(api_response)


class FrameworkApiObject:
    _OBJECT_REGISTER = {}
    _ALL_OBJECTS = set()

    def __init__(self, entity):
        self.entity = entity
        self._status = None
        self._name = None
        self._ALL_OBJECTS.add(self)

    @property
    def status(self):
        return self.entity.status

    @property
    def object_id(self):
        return self.entity.object_id

    @property
    def name(self):
        if self._name is not None:
            return self._name

        self.entity.wait(property_name="name")
        self._name = self.entity.name
        self._OBJECT_REGISTER[self._name] = self
        return self._name


class obj:

    @staticmethod
    def get(name):
        if name in FrameworkApiObject._OBJECT_REGISTER:
            return FrameworkApiObject._OBJECT_REGISTER[name]

        for fa_obj in FrameworkApiObject._ALL_OBJECTS:
            if name == fa_obj.name:
                return fa_obj

        return None
