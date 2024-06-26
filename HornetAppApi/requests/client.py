import requests, json, time, copy
from HornetAppApi.ClientClass import *
from HornetAppApi.JsonClass import *
from HornetAppApi.ApiTypes import *

class HornetClientR(HornetClientAbs):

    def __init__(self):
        HornetClientAbs.__init__(self)
        self.session = requests.Session()

    # Setters & getters:

    def set_headers(self, headers: dict):
        self.session.headers = copy.deepcopy(headers)

    def get_headers(self) -> dict:
        return copy.deepcopy(self.session.headers)

    def set_token(self, token: str):
        self.session.headers['Authorization'] = 'Hornet ' + token

    def get_token(self) -> str:
        return self.session.headers['Authorization'][7:] if 'Authorization' in self.session.headers else ''

    # protected
    
    def _do_get(self, url: str, return_type: JsonLoadable=None,
                      return_method=None, obj_name: str=None, headers: dict=None) -> any:
        headers = self.get_headers() if headers is None else headers
        if headers is False:
            respo = self.session.get(url)
        else:
            respo = self.session.get(url, headers=headers)

        self._on_response(response=respo)

        if (return_type is not None) or (return_method is not None):
            obj = respo.json()

            if return_type is not None:
                res: JsonLoadable = return_type()
                res.load_from_dict(obj if obj_name is None else obj[obj_name])
                return res

            if return_method is not None:
                res: any = return_method(obj)
                return res


    # API functions:

    @HornetClientAbs._apicall
    def get_session(self) -> HornetSession:
        resp = self.session.get(f'{API_URL}session')
        self._on_response(resp)
        obj = resp.json()
        res = HornetSession()
        res.load_from_dict(obj['session'])
        return res

    @HornetClientAbs._apicall
    def get_location_info(self) -> HornetLocationInfo:
        headers_save = self.session.headers
        headers = {}

        for name, value in headers_save.items():
            if name in ('User-Agent', 'Accept', 'Accept-Encoding'):
                headers[name] = value

        self.session.headers = headers
        try:
            resp = self.session.get(f'{HORNETAPP_URL}location-info')
        finally:
            self.session.headers = headers_save

        self._on_response(resp)
        obj = resp.json()
        res = HornetLocationInfo()
        res.load_from_dict(obj)
        return res

    @HornetClientAbs._apicall
    def set_filters(self, min_age: int, max_age: int):
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
        headers = copy.deepcopy(self.session.headers)
        headers['content-type'] = 'application/json; charset=UTF-8'
        respo = self.session.post(API_URL + 'filters.json', headers=headers, json=body)
        self._on_response(respo)

    @HornetClientAbs._apicall
    def _get_members(self, path: str, page: int = 1, per_page: int = DEF_MEMBERS_PER_PAGE) -> List[HornetPartialMember]:
        respo = self.session.get(API_URL + f'members/{path}?page={page}&per_page={per_page}')
        self._on_response(respo)
        obj = respo.json()
        return self._parse_members(obj)

    @HornetClientAbs._apicall
    def get_fans(self, page: int=1, per_page: int=25) -> List[HornetPartialMember]:
        return self._do_get(
            url=f'{API_URL}favourites/fans.json?page={page}&per_page={per_page}',
            return_method=self._parse_members)

    @HornetClientAbs._apicall
    def get_favourites(self, page: int=1, per_page: int=25) -> List[HornetPartialMember]:
        return self._do_get(
            url=f'{API_URL}favourites/favourites.json?page={page}&per_page={per_page}',
            return_method=self._parse_members)

    @HornetClientAbs._apicall
    def get_members_by_username(self, username: str, page: int = 1, per_page: int = 25) -> List[HornetPartialMember]:
        return self._do_get(
            url=f'{API_URL}members/search?username={username}&page={page}&per_page={per_page}',
            return_method=self._parse_members)

    @HornetClientAbs._apicall
    def get_members_by_hashtags(self, hashtags, page: int = 1, per_page: int = 25) -> List[HornetPartialMember]:
        return self._do_get(
            url=f'{API_URL}members/search.json?hashtags={hashtags}&page={page}&per_page={per_page}',
            return_method=self._parse_members)

    @HornetClientAbs._apicall
    def get_member(self, member_id, gallery_preview_photos: int = DEF_GALLERY_PREW_PHOTOS) -> HornetMember:
        respo = self.session.get(API_URL + f'members/{member_id}.json?gallery_preview_photos={gallery_preview_photos}')
        self._on_response(respo)
        obj = respo.json()
        res = HornetMember()
        res.load_from_dict(obj['member'])
        return res

    @HornetClientAbs._apicall
    def get_member_feed_photos(self, member_id, page: int = 1, per_page: int = DEF_MEMBERS_PER_PAGE) -> List[HornetFeedPhoto]:
        respo = self.session.get(API_URL + f'feed_photos?page={page}&per_page={per_page}&member_id={member_id}')
        self._on_response(respo)
        obj = respo.json()
        return parse_badnamed_dict_list(HornetFeedPhoto, obj, 'feed_photos', 'feed_photo')

    @HornetClientAbs._apicall
    def get_member_feeds(self, member_id, after = None, per_page: int = 10):
        params = '?'
        if after is not None:
            params = params + f'after={after}'
        params = params + f'&per_page={per_page}'

        respo = self.session.get(API_URL + f'feeds/{member_id}{params}')
        self._on_response(respo)
        obj = respo.json()
        res = HornetActivities()
        res.load_from_dict(obj)
        return res

    @HornetClientAbs._apicall
    def get_conversations(self, inbox = "primary", page: int = 1, per_page: int = 10) -> HornetConversations:
        respo = self.session.get(API_URL + f'messages/conversations.json?inbox={inbox}&page={page}&per_page={per_page}')
        self._on_response(respo)
        obj = respo.json()
        res = HornetConversations()
        res.load_from_dict(obj)
        return res

    def get_unread(self, page: int = 1, per_page: int = 10) -> HornetConversations:
        return self.get_conversations(inbox = 'unread', page = page, per_page = per_page)

    def get_requests(self, page: int = 1, per_page: int = 10) -> HornetConversations:
        return self.get_conversations(inbox = 'requests', page = page, per_page = per_page)

    @HornetClientAbs._apicall
    def get_feeds_timeline(self, after = None, per_page: int = 8):
        params = '?'
        if after is not None:
            params = params + f'after={after}'
        params = params + f'&per_page={per_page}'

        respo = self.session.get(API_URL + f'feeds/timeline{params}')
        self._on_response(respo)
        obj = respo.json()

        res = HornetActivities()
        res.load_from_dict(obj)
        return res

    @HornetClientAbs._apicall
    def delete_conversation(self, member_id) -> bool:
        respo = self.session.delete(API_URL + f'messages/{member_id}')
        self._on_response(respo)
        return respo.status_code != 404

    @HornetClientAbs._apicall
    def add_ignore_member(self, member_id) -> bool:
        obj = { "member_id": member_id, "t": 0 }
        resp = self.session.post(
            f'{API_URL}explore_ignores',
            json = obj)

        self._on_response(resp)
        return resp.status in (203, 200)

    @HornetClientAbs._apicall
    def delete_ignore_member(self, member_id) -> bool:
        resp = self.session.delete(f'{API_URL}explore_ignores/{member_id}')
        self._on_response(resp)
        return resp.status in (203, 200)

    @HornetClientAbs._apicall
    def add_block_member(self, member_id) -> bool:
        obj = { "member_id": member_id, "t": 0 }
        resp = self.session.post(
            f'{API_URL}blocks.json',
            json = obj)

        self._on_response(resp)
        obj = resp.json()
        res = obj['block']['member_id'] == member_id
        return res

    @HornetClientAbs._apicall
    def delete_block_member(self, member_id) -> bool:
        resp = self.session.delete(f'{API_URL}blocks/{member_id}')
        self._on_response(resp)
        return resp.status == 200

    @HornetClientAbs._apicall
    def get_comments(self, activity_id, before = None, after = None) -> HornetComments:
        if before is not None:
            params = f'&before={before}'
        elif after is not None:
            params = f'&after={after}'
        else:
            params = ''

        return self._do_get(
            url=f'{API_URL}activities/{activity_id}/comments.json?activity_id={activity_id}{params}',
            return_type=HornetComments)

    # def GetLookupData(self):
    #     Response = self.session.get(API_URL + f'lookup_data/all')
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

