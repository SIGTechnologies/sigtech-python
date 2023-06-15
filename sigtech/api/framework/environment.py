from sigtech.api.client.client import Client

_GLOBAL_ENVIRONMENT = None


class Environment:

    def __init__(self, client, session_id):
        self.session_id = session_id
        self.client = client
        self.object_register = {}
        self.all_objects = set()


def env():
    global _GLOBAL_ENVIRONMENT
    return _GLOBAL_ENVIRONMENT


def init():
    global _GLOBAL_ENVIRONMENT

    if _GLOBAL_ENVIRONMENT is None:
        client = Client()

        # check service
        print(client.status.get())

        # if new init or _GLOBAL_SESSION is None
        session = client.sessions.create()

        # check status

        #
        _GLOBAL_ENVIRONMENT = Environment(client, session.session_id)

    return _GLOBAL_ENVIRONMENT


class obj:

    @staticmethod
    def get(name):
        if name in env().object_register:
            return env().object_register[name]

        for fa_obj in env().all_objects:
            if name == fa_obj.name:
                return fa_obj

        return None
