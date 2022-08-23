## HornetAppApi
<img src="https://hornet.com/assets/images/favicon.ico" height="24"> [hornet.com](https://hornet.com) API wrapper

### Install
```shell
python -m pip install -e https://github.com/Kisspeace/HornetAppApi
```
### Create client and set headers
```python
from HornetAppApi import *

headers = { # from android app
    'Authorization': '',
    'Accept-Language': 'en',   # set your language
    'Accept': 'application/json',
    'X-Device-Identifier': '', # set your device id
    'X-Client-Version': 'Android 7.1.1',
    'X-Device-Name': '',       # Set your device name
    'Cache-Control': 'no-cache',
    'Host': HornetAppApi.ApiTypes.API_HOST,
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/4.8.1'
}

# client = HornetAppApi.HornetClientR() # for requests engine
client = HornetAppApi.HornetClientAio() # for aiohttp engine
client.SetHeaders(headers)
client.ApiCallTimeout = 0.485 # you can change timeout between calls
client.SetToken('') # Hornet token
```
### With aiohttp
```python
# client must be HornetClientAio
users = await client.GetMembersNear()
for u in users:
    print(f'[{u.id} {u.account_username }] name: "{u.display_name}" age: {u.age}')
```

### With requests
```python
# client must be HornetClientR
users = client.GetMembersNear()
for u in users:
    print(f'[{u.id} {u.account_username }] name: "{u.display_name}" age: {u.age}')
```

### capabilities
* ✔️ Search users near
* ✔️ Search users recent
* ✔️ Search users by hashtags
* ✔️ Search users by name
* ✔️ Get user by id
* ✔️ Get user feeds
* ✔️ Get user feed photos
* ✔️ Get feeds timeline
* ✔️ Get conversations
* ✔️ Get unread conversations
* ✔️ Delete conversation
* ➖ Set search filters (only min and max age)
* ❌ Send messages
* ❌ Create posts
* ❌ Create comments
* ❌ Add photos
* ❌ Follow user
* ❌ Unfollow user
