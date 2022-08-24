import requests, json, time, copy
from HornetAppApi import *

class HornetClientR(HornetClientAbs):

    def __init__(self):
        HornetClientAbs.__init__(self)
        self.Session = requests.Session()

    # Setters & getters:

    def SetHeaders(self, headers):
        self.Session.headers = copy.deepcopy(headers)

    def GetHeaders(self) -> dict:
        return copy.deepcopy(self.Session.headers)

    def SetToken(self, token: str):
        self.Session.headers['Authorization'] = 'Hornet ' + token

    def GetToken(self) -> str:
        return self.Session.headers['Authorization'][7:]

    # API functions:

    @HornetClientAbs._ApiCall
    def SetFilters(self, minAge, maxAge):
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
        headers = copy.deepcopy(self.Session.headers)
        headers['content-type'] = 'application/json; charset=UTF-8'
        respo = self.Session.post(API_URL + 'filters.json', headers=headers, json=body)
        self._DoOnResponse(respo)

    @HornetClientAbs._ApiCall
    def _GetMembers(self, path: str, page = 1, perPage = DEF_MEMBERS_PER_PAGE) -> list:
        respo = self.Session.get(API_URL + f'members/{path}?page={page}&per_page={perPage}')
        self._DoOnResponse(respo)
        js = respo.json()
        return self._ParseMembers(js) 

    @HornetClientAbs._ApiCall
    def GetMembersByUsername(self, username: str, page = 1, perPage = 25) -> list:
        respo = self.Session.get(API_URL + f'members/search?username={username}&page={page}&per_page={perPage}')
        self._DoOnResponse(respo)
        js = respo.json()
        return self._ParseMembers(js)

    @HornetClientAbs._ApiCall
    def GetMember(self, id, gallery_preview_photos = DEF_GALLERY_PREW_PHOTOS) -> HornetMember:
        respo = self.Session.get(API_URL + f'members/{id}.json?gallery_preview_photos={gallery_preview_photos}')
        self._DoOnResponse(respo)
        js = respo.json()
        Result = HornetMember()
        Result.LoadFromDict(js['member'])
        return Result

    @HornetClientAbs._ApiCall
    def GetMemberFeedPhotos(self, memberId, page = 1, perPage = DEF_MEMBERS_PER_PAGE):
        respo = self.Session.get(API_URL + f'feed_photos?page={page}&per_page={perPage}&member_id={memberId}')
        self._DoOnResponse(respo)
        js = respo.json()
        return ParseBadNamedDictList(HornetFeedPhoto, js, 'feed_photos', 'feed_photo')
     
    @HornetClientAbs._ApiCall 
    def GetMemberFeeds(self, memberId, after = None, perPage = 10):
        params = '?'
        if (after != None):
            params = params + f'after={after}'
        params = params + f'&per_page={perPage}'

        respo = self.Session.get(API_URL + f'feeds/{memberId}{params}')
        self._DoOnResponse(respo)
        js = respo.json()
        res = HornetActivities()
        res.LoadFromDict(js)
        return res

    @HornetClientAbs._ApiCall
    def GetConversations(self, inbox = "primary", page = 1, perPage = 10) -> HornetConversations:
        respo = self.Session.get(API_URL + f'messages/conversations.json?inbox={inbox}&page={page}&per_page={perPage}')
        self._DoOnResponse(respo)
        js = respo.json()
        Result = HornetConversations()
        Result.LoadFromDict(js)          
        return Result

    @HornetClientAbs._ApiCall
    def GetUnread(self, page = 1, perPage = 10) -> HornetConversations:
        return self.GetConversations(inbox = 'unread', page = page, perPage = perPage)

    @HornetClientAbs._ApiCall
    def GetFeedsTimeline(self, after = None, perPage = 8):
        params = '?'
        if (after != None):
            params = params + f'after={after}'
        params = params + f'&per_page={perPage}'
        respo = self.Session.get(API_URL + f'feeds/timeline{params}')
        self._DoOnResponse(respo)
        js = respo.json() 

        res = HornetActivities()
        res.LoadFromDict(js)
        return res
    
    @HornetClientAbs._ApiCall
    def DeleteConversation(self, memberId) -> bool:
        respo = self.Session.delete(API_URL + f'messages/{memberId}')
        self._DoOnResponse(respo)
        return (respo.status_code != 404)
        

    # def GetLookupData(self):
    #     Response = self.Session.get(API_URL + f'lookup_data/all')
    #     Js = Response.json()
    #     save_dump('GetLookupData', Js) 

    
    # def Send(self, memberId, data = None, type = "chat"): # Android like
    #     Js = {
    #         "client_ref": str(uuid.uuid4()), 
    #         "real_id": str(uuid.uuid4()), 
    #         "sender": int(memberId),
    #         "type": "receipt"
    #     }
    #     self.Session.headers['content-type'] = 'application/json; charset=UTF-8'
    #     Response = self.Session.post(API_URL + 'messages.json', json=Js)
    #     Js = Response.json()
    #     if (Response.status_code != 201):
    #         exit

    #     Js = {
    #         "message":{
    #             "client_ref": str(uuid.uuid4()), 
    #             "data": str(data),
    #             "created_at": str(datetime.now().isoformat()),
    #             "is_deletable": None,
    #             "real_id": None,
    #             "recipient": int(memberId),
    #             "sender": senderId,
    #             "type": str(type)
    #         },
    #         "n": str(uuid.uuid4()), 
    #         "s": str(secrets.token_bytes(32).hex()), 
    #         "t": int(math.trunc(time.time()))
    #     }

    #     self.Session.headers['content-type'] = 'application/json; charset=UTF-8'
    #     Response = self.Session.post(API_URL + 'messages.json', json=Js)
    #     Js = Response.json()
    #     return Js

