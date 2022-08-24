from HornetAppApi import *
import asyncio, aiohttp
import json, time, copy

class HornetClientAio(HornetClientAbs):
    def __init__(self):
        HornetClientAbs.__init__(self)
        self._headers = {}
    
    # Setters & getters:

    def SetHeaders(self, headers):
        self._headers = copy.deepcopy(headers)

    def GetHeaders(self) -> dict:
        return copy.deepcopy(self._headers)

    def SetToken(self, token: str):
        self._headers['Authorization'] = 'Hornet ' + token

    def GetToken(self) -> str:
        return self._headers['Authorization']

    # protected
    
    async def _DoOnResponse(self, response):
        if callable(self.OnResponse):
            await self.OnResponse(self, response)

    def _ApiCall(func):
        async def inner(self, *args, **kwargs):
            t = self.GetCurrentTimeout()
            if (t > 0):
                # print('sleep: ', t)
                await asyncio.sleep(t)
            
            result = await func(self, *args, **kwargs)
            self._LastApiCallTime = time.time()
            # print(f'{func.__name__} finished at: {self._LastApiCallTime}')
            return result
        return inner

    # API functions:

    @_ApiCall
    async def SetFilters(self, minAge, maxAge):
        body = {
            "filters": [
                    {
                        "filter": {
                            "category": "general", 
                            "key": "age",
                            "data": {
                                "max": int(maxAge),
                                "min": int(minAge)
                            }
                        }
                    }
                ]
        }
        headers = self.GetHeaders()
        headers['content-type'] = 'application/json; charset=UTF-8'
        async with aiohttp.ClientSession() as session:
            respo = await session.post(
                f'{API_URL}filters.json', 
                headers = headers, 
                json = body
            )

    @_ApiCall
    async def _GetMembers(self, path: str, page = 1, perPage = DEF_MEMBERS_PER_PAGE) -> list:
        async with aiohttp.ClientSession() as session:
            respo = await session.get(
                f'{API_URL}members/{path}?page={page}&per_page={perPage}', 
                headers = self._headers
            ) 

            await self._DoOnResponse(respo)
            js = await respo.json()

        return self._ParseMembers(js)

    async def GetMembersNear(self, page = 1, perPage = DEF_MEMBERS_PER_PAGE) -> list:
        return await self._GetMembers(path='near', page=page, perPage=perPage)

    async def GetMembersRecent(self, page = 1, perPage = DEF_MEMBERS_PER_PAGE) -> list:
        return await self._GetMembers(path='recent', page=page, perPage=perPage)
     
    @_ApiCall 
    async def GetMembersByUsername(self, username: str, page = 1, perPage = 25) -> list:
        async with aiohttp.ClientSession() as session:
            respo = await session.get(
                f'{API_URL}members/search?username={username}&page={page}&per_page={perPage}', 
                headers = self._headers
            )

            await self._DoOnResponse(respo)
            js = await respo.json()

        return self._ParseMembers(js)
    
    @_ApiCall
    async def GetMembersByHashtags(self, hashtags, page = 1, perPage = 25) -> list:
        async with aiohttp.ClientSession() as session:
            respo = await session.get(
                f'{API_URL}members/search.json?hashtags={hashtags}&page={page}&per_page={perPage}',
                headers = self._headers
            )
            await self._DoOnResponse(respo)
            js = await respo.json()
            return self._ParseMembers(js)

    @_ApiCall
    async def GetMember(self, id, gallery_preview_photos = DEF_GALLERY_PREW_PHOTOS) -> HornetMember:
        async with aiohttp.ClientSession() as session:
            respo = await session.get(
                f'{API_URL}members/{id}.json?gallery_preview_photos={gallery_preview_photos}', 
                headers = self._headers
            )
            
            await self._DoOnResponse(respo)
            js = await respo.json()

        Result = HornetMember()
        Result.LoadFromDict(js['member'])
        return Result

    @_ApiCall
    async def GetMemberFeedPhotos(self, memberId, page = 1, perPage = DEF_MEMBERS_PER_PAGE) -> list:
        async with aiohttp.ClientSession() as session:
            respo = await session.get(
                f'{API_URL}feed_photos?page={page}&per_page={perPage}&member_id={memberId}', 
                headers = self._headers
            )
            
            await self._DoOnResponse(respo)
            js = await respo.json()

        return ParseBadNamedDictList(HornetFeedPhoto, js, 'feed_photos', 'feed_photo')

    @_ApiCall
    async def GetConversations(self, inbox = "primary", page = 1, perPage = 10) -> HornetConversations:
        async with aiohttp.ClientSession() as session:
            respo = await session.get(
                f'{API_URL}messages/conversations.json?inbox={inbox}&page={page}&per_page={perPage}', 
                headers = self._headers
            )

        await self._DoOnResponse(respo)
        js = await respo.json()

        Result = HornetConversations()
        Result.LoadFromDict(js)          
        return Result
    
    async def GetUnread(self, page = 1, perPage = 10) -> HornetConversations:
        return await self.GetConversations(inbox = 'unread', page = page, perPage = perPage)

    @_ApiCall
    async def GetMemberFeeds(self, memberId, after = None, perPage = 10):
        params = '?'
        if (after != None):
            params = params + f'after={after}'
        params = params + f'&per_page={perPage}'

        async with aiohttp.ClientSession() as session:
            respo = await session.get(
                f'{API_URL}feeds/{memberId}{params}',
                headers = self._headers
            )

        await self._DoOnResponse(respo)
        js = await respo.json()

        res = HornetActivities()
        res.LoadFromDict(js)
        return res

    @_ApiCall
    async def GetFeedsTimeline(self, after = None, perPage = 8) -> HornetActivities:
        params = '?'
        if (after != None):
            params = params + f'after={after}'
        params = params + f'&per_page={perPage}'
        
        async with aiohttp.ClientSession() as session: 
            respo = await session.get(
                f'{API_URL}feeds/timeline{params}',
                headers = self._headers
            )
        
        await self._DoOnResponse(respo)
        js = await respo.json() 

        res = HornetActivities()
        res.LoadFromDict(js)
        return res

    @_ApiCall
    async def DeleteConversation(self, memberId) -> bool:
        async with aiohttp.ClientSession() as session:
            respo = await session.delete(
                f'{API_URL}messages/{memberId}', 
                headers = self._headers
            )

        self._DoOnResponse(respo)
        return (respo.status != 404)
