from HornetAppApi import *
import asyncio, aiohttp
import json, time, copy

class HornetClientAio(HornetClientAbs):
    def __init__(self):
        HornetClientAbs.__init__(self)
        self._headers = {}

    # Setters & getters:

    def set_headers(self, headers: dict):
        self._headers = copy.deepcopy(headers)

    def get_headers(self) -> dict:
        return copy.deepcopy(self._headers)

    def set_token(self, token: str):
        self._headers['Authorization'] = 'Hornet ' + token

    def get_token(self) -> str:
        return self._headers['Authorization'][7:] if 'Authorization' in self._headers else ''

    # protected

    async def _do_get(self, url: str, return_type: JsonLoadable=None,
                      return_method=None, obj_name: str=None, headers: dict=None) -> any:
        headers = self._headers if headers is None else headers
        async with aiohttp.ClientSession() as session:
            if headers == False:
                respo = await session.get(url)
            else:
                respo = await session.get(url, headers=headers)

        await self._on_response(response=respo)

        if (return_type is not None) or (return_method is not None):
            obj = await respo.json()

            if return_type is not None:
                res: JsonLoadable = return_type()
                res.load_from_dict(obj if obj_name is None else obj[obj_name])
                return res

            if return_method is not None:
                res: any = return_method(obj)
                return res


    async def _on_response(self, response):
        if callable(self.event_response):
            await self.event_response(self, response)

    def _apicall(func):
        async def inner(self, *args, **kwargs):
            t = self.get_current_timeout()
            if t > 0:
                await asyncio.sleep(t)

            result = await func(self, *args, **kwargs)
            self._last_apicall_time = time.time()
            return result
        return inner

    # API functions:

    @_apicall
    async def get_session(self) -> HornetSession:
        return await self._do_get(
            url=f'{API_URL}session',
            return_type=HornetSession,
            obj_name='session')

    @_apicall
    async def get_location_info(self) -> HornetLocationInfo:
        headers: dict = {}
        if 'User-Agent' in self._headers:
            headers['User-Agent'] = self._headers['User-Agent']
            
        return await self._do_get(
            url=f'{HORNETAPP_URL}location-info',
            return_type=HornetLocationInfo,
            headers=headers)

    @_apicall
    async def set_filters(self, min_age: int, max_age: int):
        body = {
            "filters": [
                    {
                        "filter": {
                            "category": "general", 
                            "key": "age",
                            "data": {
                                "max": int(max_age),
                                "min": int(min_age)
                            }
                        }
                    }
                ]
        }
        headers = self.get_headers()
        headers['content-type'] = 'application/json; charset=UTF-8'
        async with aiohttp.ClientSession() as session:
            respo = await session.post(
                f'{API_URL}filters.json',
                headers = headers,
                json = body
            )

    @_apicall
    async def _get_members(self, path: str, page: int = 1, per_page: int = DEF_MEMBERS_PER_PAGE) -> List[HornetPartialMember]:
        return await self._do_get(
            url=f'{API_URL}members/{path}?page={page}&per_page={per_page}',
            return_method=self._parse_members)

    async def get_members_near(self, page: int = 1, per_page: int = DEF_MEMBERS_PER_PAGE) -> List[HornetPartialMember]:
        return await self._get_members(path='near', page=page, per_page=per_page)

    async def get_members_recent(self, page = 1, per_page = DEF_MEMBERS_PER_PAGE) -> List[HornetPartialMember]:
        return await self._get_members(path='recent', page=page, per_page=per_page)

    async def get_members_viewed_me(self, page: int=1, per_page: int= DEF_MEMBERS_PER_PAGE) -> List[HornetPartialMember]:
        return await self._get_members(path='viewed_me', page=page, per_page=per_page)

    @_apicall
    async def get_fans(self, page: int=1, per_page: int=25) -> List[HornetPartialMember]:
        return await self._do_get(
            url=f'{API_URL}favourites/fans.json?page={page}&per_page={per_page}',
            return_method=self._parse_members)

    @_apicall
    async def get_favourites(self, page: int=1, per_page: int=25) -> List[HornetPartialMember]:
        return await self._do_get(
            url=f'{API_URL}favourites/favourites.json?page={page}&per_page={per_page}',
            return_method=self._parse_members)

    @_apicall
    async def get_members_by_username(self, username: str, page: int = 1, per_page: int = 25) -> List[HornetPartialMember]:
        return await self._do_get(
            url=f'{API_URL}members/search?username={username}&page={page}&per_page={per_page}',
            return_method=self._parse_members)

    @_apicall
    async def get_members_by_hashtags(self, hashtags, page: int = 1, per_page: int = 25) -> List[HornetPartialMember]:
        return await self._do_get(
            url=f'{API_URL}members/search.json?hashtags={hashtags}&page={page}&per_page={per_page}',
            return_method=self._parse_members)

    @_apicall
    async def get_member(self, member_id, gallery_preview_photos = DEF_GALLERY_PREW_PHOTOS) -> HornetMember:
        return await self._do_get(
            url=f'{API_URL}members/{member_id}.json?gallery_preview_photos={gallery_preview_photos}',
            return_type=HornetMember,
            obj_name='member')

    @_apicall
    async def get_member_feed_photos(self, member_id, page: int = 1,
                                     per_page: int = DEF_MEMBERS_PER_PAGE) -> List[HornetFeedPhoto]:
        return await self._do_get(
            url=f'{API_URL}feed_photos?page={page}&per_page={per_page}&member_id={member_id}',
            return_method=self._parse_feed_photos)

    @_apicall
    async def get_conversations(self, inbox: str = "primary", page: int = 1, per_page: int = 10) -> HornetConversations:
        return await self._do_get(
            url=f'{API_URL}messages/conversations.json?inbox={inbox}&page={page}&per_page={per_page}',
            return_type=HornetConversations)
    
    async def get_unread(self, page: int = 1, per_page: int = 10) -> HornetConversations:
        return await self.get_conversations(inbox = 'unread', page = page, per_page = per_page)
    
    async def get_requests(self, page: int = 1, per_page: int = 10) -> HornetConversations:
        return await self.get_conversations(inbox = 'requests', page = page, per_page = per_page)
    
    @_apicall
    async def get_member_feeds(self, member_id, after = None, per_page: int = 10) -> HornetActivities:
        params = '?'
        if after is not None:
            params = params + f'after={after}'
        params = params + f'&per_page={per_page}'

        return await self._do_get(
            url=f'{API_URL}feeds/{member_id}{params}',
            return_type=HornetActivities)

    @_apicall
    async def get_feeds_timeline(self, after = None, per_page: int = 8) -> HornetActivities:
        params = '?'
        if after is not None:
            params = params + f'after={after}'
        params = params + f'&per_page={per_page}'

        return await self._do_get(
            url=f'{API_URL}feeds/timeline{params}',
            return_type=HornetActivities)

    @_apicall
    async def delete_conversation(self, member_id) -> bool:
        async with aiohttp.ClientSession() as session:
            respo = await session.delete(
                f'{API_URL}messages/{member_id}', 
                headers = self._headers
            )

        self._on_response(respo)
        return respo.status != 404

    @_apicall
    async def add_ignore_member(self, member_id) -> bool:
        obj = { "member_id": member_id, "t": 0 }
        async with aiohttp.ClientSession() as session:
            resp = await session.post(
                f'{API_URL}explore_ignores',
                headers = self._headers,
                json = obj)

            await self._on_response(resp)
            return resp.status in (203, 200)

    @_apicall
    async def delete_ignore_member(self, member_id) -> bool:
        async with aiohttp.ClientSession() as session:
            resp = await session.delete(
                f'{API_URL}explore_ignores/{member_id}',
                headers = self._headers)

            await self._on_response(resp)
            return resp.status in (203, 200)

    @_apicall
    async def add_block_member(self, member_id) -> bool:
        obj = { "member_id": member_id, "t": 0 }
        async with aiohttp.ClientSession() as session:
            resp = await session.post(
                f'{API_URL}blocks.json',
                headers = self._headers,
                json = obj)

            await self._on_response(resp)
            obj = await resp.json()
            res = obj['block']['member_id'] == member_id
            return res

    @_apicall
    async def delete_block_member(self, member_id) -> bool:
        async with aiohttp.ClientSession() as session:
            resp = await session.delete(
                f'{API_URL}blocks/{member_id}',
                headers = self._headers)

            await self._on_response(resp)
            return resp.status == 200
        
    @_apicall
    async def get_comments(self, activity_id, before = None, after = None) -> HornetComments:
        if before is not None:
            params = f'&before={before}'
        elif after is not None:
            params = f'&after={after}'
        else:
            params = ''

        return await self._do_get(
            url=f'{API_URL}activities/{activity_id}/comments.json?activity_id={activity_id}{params}',
            return_type=HornetComments)