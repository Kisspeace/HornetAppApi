import HornetAppApi
import copy, sys, time, asyncio, random, json, inspect
from HornetAppApi import *

client = None
engine = 'aiohttp'
TEST_USER_ID = 0
TEST_USERNAME = '1d'
PRINT_DATA = False


def islistof(alist: list, type) -> bool:
    if (isinstance(alist, list) != True):
        return False
    if (len(alist) > 0):
        return isinstance(alist[0], type)
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
        print('is list of')
        l = []
        for i in a:
            print('vkusno', type(i))
            l.append(ObjToDict(i))
        a = l
    else:
        print('is other')
        a = ObjToDict(a)

    return json.dumps(a, indent = 4)

def writeln(a):
    if (isinstance(a, JsonLoadable) or islistof(a, JsonLoadable)):
        print(js(a))
    else:
        print(a)

def calc_time(func):
    def inner(*args, **kwargs):
        started_at = time.time()
        result = func(*args, **kwargs)
        finished_at = time.time()
        elapsed = (finished_at - started_at)
        print(f'{func.__name__}: {elapsed} sec.')
        return result, elapsed
    return inner

def test(func, name = ''):
    global current_func
    global PRINT_DATA
    global client

    def OnResponse(sender, response):
        js = response.json()
        save_dump(f'{sender.__class__.__name__}_{name}', data=js)

    async def OnResponseAsync(sender, response):
        js = await response.json()
        save_dump(f'{sender.__class__.__name__}_{name}', data=js)

    def set_event():
        if isinstance(client, HornetAppApi.HornetClientAio):
            client.OnResponse = OnResponseAsync
        else:
            client.OnResponse = OnResponse

    def after(res):
        print(f'{name} result: ', type(res))
        if PRINT_DATA:
            writeln(res)

    async def innerAsync(*args, **kwargs):
        set_event()
        result = await func(*args, **kwargs)
        after(result)    
        return result
    
    def inner(*args, **kwargs):
        set_event()
        result = func(*args, **kwargs)
        after(result)    
        return result

    def save_dump(name: str, data): 
        f = open(f'dump_{name}_{time.time()}.json', 'w')
        if isinstance(data, dict):
            f.write(json.dumps(data, indent = 4))
        else:
            f.write(str(data))
        f.close()

    if isinstance(client, HornetAppApi.HornetClientAio):
        return innerAsync
    else:
        return inner

def CreateClient(engine_name):
    if (engine_name == 'requests'):
        return HornetAppApi.HornetClientR()
    elif (engine_name == 'aiohttp'):
        return HornetAppApi.HornetClientAio()
    else:
        return None

async def test_async():
    global engine
    global client
    global TEST_USER_ID
    global TEST_USERNAME

    await test(client.GetMembersByHashtags, 'GetMembersByHashtags')(hashtags='transgender')
    await test(client.GetMember, 'GetMember')(TEST_USER_ID)
    await test(client.GetMembersNear, 'GetMembersNear')()
    await test(client.GetMembersRecent, 'GetMembersRecent')()
    await test(client.GetMembersByUsername, 'GetMembersByUsername')(username=TEST_USERNAME)
    await test(client.GetMemberFeedPhotos, 'GetMemberFeedPhotos')(memberId=TEST_USER_ID)
    await test(client.GetUnread, 'GetUnread')()
    await test(client.GetMemberFeeds, 'GetMemberFeeds')(TEST_USER_ID)
    await test(client.GetFeedsTimeline, 'GetFeedsTimeline')()
    await test(client.SetFilters, 'SetFilters')(0, 100)

async def async_main():
    await asyncio.wait([
        asyncio.create_task(test_async())
    ])

if len(sys.argv) > 1:
    engine = sys.argv[1]
print(f'Test for {engine}:')

client = CreateClient(engine)
headers = {
    'Authorization': '',
    'Accept-Language': 'en', # set yout language
    'Accept': 'application/json',
    'X-Device-Identifier': '', # set yout device id
    'X-Client-Version': 'Android 7.1.1',
    'X-Device-Name': '', # Set yout device name
    'Cache-Control': 'no-cache',
    'Host': HornetAppApi.ApiTypes.API_HOST,
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'User-Agent': 'okhttp/4.8.1'
}
client.SetHeaders(headers)
client.ApiCallTimeout = 0.485
client.SetToken('') # TOKEN HERE

if (client.GetToken() == ''):
    print('Please set token!')
    exit()

if isinstance(client, HornetClientAio):
    asyncio.run(async_main())
else:
    test(client.GetMembersByHashtags, 'GetMembersByHashtags')(hashtags='transgender')
    test(client.GetMember, 'GetMember')(TEST_USER_ID)
    test(client.GetMembersNear, 'GetMembersNear')()
    test(client.GetMembersRecent, 'GetMembersRecent')()
    test(client.GetMembersByUsername, 'GetMembersByUsername')(username=TEST_USERNAME)
    test(client.GetMemberFeedPhotos, 'GetMemberFeedPhotos')(memberId=TEST_USER_ID)
    test(client.GetUnread, 'GetUnread')()
    test(client.GetMemberFeeds, 'GetMemberFeeds')(TEST_USER_ID)
    test(client.GetFeedsTimeline, 'GetFeedsTimeline')()
    test(client.SetFilters, 'SetFilters')(0, 100)

print('fin')
