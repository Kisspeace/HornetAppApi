## HornetAppApi
<img src="https://hornet.com/assets/images/favicon.ico" height="24"> [hornet.com](https://hornet.com) API wrapper

### Install
```shell
python -m pip install -e "git+https://github.com/Kisspeace/HornetAppApi.git#egg=HornetAppApi" 
```
### Create client and set headers
```python
import HornetAppApi

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
client.set_headers(headers)
client.apicall_timeout = 0.485 # you can change timeout between calls
client.set_token('') # Hornet token
```
### With aiohttp
```python
# client must be HornetClientAio
users = await client.get_members_near()
for u in users:
    print(f'[{u.id} {u.account.username}] name: "{u.display_name}" age: {u.age}')
```

### With requests
```python
# client must be HornetClientR
users = client.get_members_near()
for u in users:
    print(f'[{u.id} {u.account.username}] name: "{u.display_name}" age: {u.age}')
```

### capabilities
* ✔️ Search users near
* ✔️ Search users recent
* ✔️ Search users by hashtags
* ✔️ Search users by name
* ✔️ Get users who checked you
* ✔️ Get user by id
* ✔️ Get user feeds
* ✔️ Get user feed photos
* ✔️ Get feeds timeline
* ✔️ Get comments
* ✔️ Get conversations
* ✔️ Get unread conversations
* ✔️ Delete conversation
* ✔️ Ignore list - add or delete user
* ✔️ Black list - add or delete user
* ➖ Set search filters (only min and max age)
* ❌ Send messages
* ❌ Create posts
* ❌ Create comments
* ❌ Add photos
* ❌ Follow user
* ❌ Unfollow user
