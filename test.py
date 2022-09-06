import HornetAppApi
import sys, time, asyncio, json
from HornetAppApi import *
import inspect
import os
import datetime

client: HornetAppApi.HornetClientAbs = None
ENGINE = 'aiohttp'

TEST_USER_ID = 0
TEST_USER_IGNORE_ID = 0
TEST_USER_BLOCK_ID = 0
TEST_USERNAME = 't'
TEST_ACTIVITY_ID = 0

TEST_DANGEROUS = False # features like: block users, ignore users
PRINT_DATA = False
PAUSE_AFTER_CALL = False
APICALL_TIMEOUT = 0.485

DUMPS_DIR = 'test-dumps'

TOKEN: str = '' # hornet token
HEADERS = { # headers from oficial android client
    'Authorization': '',
    'Accept-Language': 'en', # set yout language
    'Accept': 'application/json',
    'X-Device-Identifier': '', # set your device id
    'X-Client-Version': 'Android 7.1.1',
    'X-Device-Name': '', # Set yout device name
    'Cache-Control': 'no-cache',
    'Host': HornetAppApi.ApiTypes.API_HOST,
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/4.8.1'
}


def islistof(alist: list, atype) -> bool:
    if not isinstance(alist, list):
        return False
    if len(alist) > 0:
        return isinstance(alist[0], atype)
    else:
        return False


def ObjToDict(obj: object) -> dict:
    result = obj.__dict__
    for name, value in result.items():
        if isinstance(value, JsonLoadable):
            result[name] = ObjToDict(value)
        if islistof(value, JsonLoadable):
            result[name] = []
            for i in value:
                if isinstance(i, JsonLoadable):
                    result[name].append(ObjToDict(i))
    return result


def js(a) -> str:
    if islistof(a, JsonLoadable):
        l = []
        for i in a:
            l.append(ObjToDict(i))
        a = l
    else:
        a = ObjToDict(a)

    return json.dumps(a, indent = 4)


def writeln(a):
    if (isinstance(a, JsonLoadable) or islistof(a, JsonLoadable)):
        print(js(a))
    else:
        print(a)


def test(func, name = ''):

    def make_save(sender, obj):
        save_dump(f'{sender.__class__.__name__}_{name}', data=obj)

    def on_response(sender, response):
        try:
            obj = response.json()
            make_save(sender, obj)
        except Exception as e:
            print(f'on_response: error {e}')

    async def on_response_async(sender, response): # is dead sometimes 
        try:
            # print('on_response_async: before await response.json()')
            obj = await response.json()
            # print('on_response_async: before make_save')
            make_save(sender, obj)
        except Exception as e:
            print(f'on_response_async: error {e}')

    def set_event():
        if isinstance(client, HornetAppApi.HornetClientAio):
            client.event_response = on_response_async
        else:
            client.event_response = on_response

    def after(res):
        print(f'{name} result: ', type(res))
        if PRINT_DATA:
            writeln(res)
        if PAUSE_AFTER_CALL:
            input()
        if (isinstance(res, JsonLoadable) or
           (isinstance(res, list) and len(res) > 0)):
                save_dump(f'_{name}', data=js(res), prefix='fromobj')

    async def inner_async(*args, **kwargs):
        set_event()
        result = await func(*args, **kwargs)
        after(result)
        return result

    def inner(*args, **kwargs):
        set_event()
        result = func(*args, **kwargs)
        after(result)
        return result

    def save_dump(name: str, data, prefix: str = 'dump'):
        filename: str = f'{prefix}_{name}_{time.time()}.json'
        filename = os.path.join(DUMPS_SUBDIR, filename)
        os.makedirs(DUMPS_SUBDIR, mode = 0o777, exist_ok = True)

        file = open(filename, 'w')
        if isinstance(data, dict):
            file.write(json.dumps(data, indent=4))
        else:
            file.write(str(data))
        file.close()

    if isinstance(client, HornetAppApi.HornetClientAio):
        return inner_async
    else:
        return inner


async def go(func, func_name: str, *args, **kwargs):
    if inspect.isawaitable(func) or isinstance(client, HornetClientAio):
        return await test(func, func_name)(*args, **kwargs)
    else:
        return test(func, func_name)(*args, **kwargs)


def new_client(engine_name):
    if engine_name == 'requests':
        return HornetAppApi.HornetClientR()
    elif engine_name == 'aiohttp':
        return HornetAppApi.HornetClientAio()
    else:
        return None


async def test_async():

    if TEST_DANGEROUS:
        await go(client.add_ignore_member, 'add_ignore_member', TEST_USER_IGNORE_ID)
        await go(client.delete_ignore_member, 'delete_ignore_member', TEST_USER_IGNORE_ID)

        await go(client.add_block_member, 'add_block_member', TEST_USER_BLOCK_ID)
        await go(client.delete_block_member, 'delete_block_member', TEST_USER_BLOCK_ID)

    await go(client.get_fans, 'get_fans')
    await go(client.get_favourites, 'get_favourites')
    await go(client.get_conversations, 'get_conversations')
    await go(client.get_requests, 'get_requests')
    await go(client.get_unread, 'get_unread')
    await go(client.get_location_info, 'get_location_info')
    await go(client.get_session, 'get_session')
    await go(client.get_comments, 'get_comments', TEST_ACTIVITY_ID)
    await go(client.get_member, 'get_member', TEST_USER_ID)
    await go(client.get_members_near, 'get_members_near')
    await go(client.get_members_recent, 'get_members_recent')
    await go(client.get_members_by_hashtags, 'get_members_by_hashtags', hashtags='transgender')
    await go(client.get_members_by_username, 'get_members_by_username', username=TEST_USERNAME)
    await go(client.get_member_feed_photos, 'get_member_feed_photos', member_id=TEST_USER_ID)
    await go(client.get_member_feeds, 'get_member_feeds', TEST_USER_ID)
    await go(client.get_feeds_timeline, 'get_feeds_timeline')
    await go(client.set_filters, 'set_filters', min_age=0, max_age=100)


if len(sys.argv) > 1:
    ENGINE = sys.argv[1]
print(f'Test for {ENGINE}:')

DUMPS_SUBDIR = os.path.join(DUMPS_DIR, f'{ENGINE}-{datetime.datetime.now()}')

client = new_client(ENGINE)
client.set_headers(HEADERS)
client.apicall_timeout = APICALL_TIMEOUT
client.set_token(TOKEN)

if client.get_token() == '':
    print('Please set token!')
    exit()

asyncio.run(test_async())
print('fin')
