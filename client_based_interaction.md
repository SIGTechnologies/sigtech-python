# Client based SDK interaction
Client based interaction is intended for users who require more low level access to the API.

## Key differences between object-level and client-based interaction

Object-based method:

- Initialization of the session is abstracted away, handled by the SDK.
- Uses higher-level objects like `sig.RollingFutureStrategy`.
- Parameters are passed directly to the object's constructor.
- Method calls are made directly on the object.
- Provides a simpler and more concise way to interact with the API.

Client-based method:

- Requires explicit setup of a client object.
- Involves creating a session and obtaining a session ID.
- Uses methods provided by the client to perform actions.
- Requires passing parameters to the methods individually.
- Involves handling status checks and waiting for operations to complete.
- Provides more fine-grained control and access to low-level API functionality.

## Example of client-based interaction

```python
# Import the SigTech API
import sigtech.api as sig

# Setup the Client
client = sig.Client()

# Create a new session and generate a new sessionId
session = client.sessions.create()
session_id = session.session_id
print(f'session id : {session_id}')

# Define the parameters of your Rolling Futures Strategy and generate an objectId
rfs = client.strategies.futures.rolling.create(
    session_id=session_id, 
    identifier='ES INDEX',
    currency='USD',
    rollingRule='front',
    frontOffset='-6:-2',
    startDate='2020-01-28'  
    )
object_id = rfs.object_id
print(f'object id : {object_id}')

# Query the status of your Rolling Futures Strategy object using its objectId
object_state = client.query_object(session_id, object_id)
print(f'object state : {object_state}')

# Wait until the "status" of your objectId is "SUCCEEDED"
rfs.wait_for_object_status()

# Retrieve the history of your Rolling Futures Strategy 
history = client.data.history.get(
    session_id=session_id, 
    object_id=object_id).history
    print(f'Rolling Future History : {history}'
    )
```