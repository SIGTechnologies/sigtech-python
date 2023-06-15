import sigtech.api as sig

sig.ClientSettings.SIGTECH_API_URL = 'https://xmqdm2hbbb.execute-api.eu-west-1.amazonaws.com/prod'
sig.ClientSettings.SIGTECH_API_KEY = 'none'
sig.ClientSettings.SIGTECH_API_WAIT_TIMER = False

# Setup Client

client = sig.Client()

# Create session

session = client.sessions.create()
session_id = session.session_id
print(f'session id : {session_id}')

# New Rolling Future Strategy Object

rfs_object = client.strategies.futures.rolling.create(
            session_id=session_id, identifier='ES INDEX', front_offset='-3:-1', rolling_rule='front'
)
object_id = rfs_object.object_id
print(f'object id : {object_id}')

# Query object status
object_state = client.query_object(session_id, object_id)
print(f'object state : {object_state}')

# wait for completion
rfs_object.wait_for_object_status()

# Retrieve history
history = client.data.history.get(session_id=session_id, object_id=object_id).history
print(f'Rolling Future History : {history}')

