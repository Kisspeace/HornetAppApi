import time
from .JsonClass import *
from .ApiTypes import *

class HornetClientAbs:
    def __init__(self):
        self.apicall_timeout: float = 0.380 # 380 ms. set 0 to disable
        # self.LastResponse = None
        # public events
        self.event_response = None # reference to procedure (sender: HornetClientAbs, response)
        # protected
        self._last_apicall_time: float = None

    # Setters & getters:

    def set_headers(self, headers: dict):
        pass

    def get_headers(self) -> dict:
        pass

    def set_token(self, token: str):
        pass

    def get_token(self) -> str:
        pass

    def get_current_timeout(self) -> float:
        result: float = 0
        if ((self._last_apicall_time is not None) and
            (self.apicall_timeout > 0)):
            t = (time.time() - self._last_apicall_time)
            result = (self.apicall_timeout - t) if (t < self.apicall_timeout) else 0
        return result

    # protected

    def _on_response(self, response):
        if callable(self.event_response):
            self.event_response(self, response)

    def _parse_members(self, source: dict) -> list:
        return parse_badnamed_dict_list(HornetPartialMember, source, 'members', 'member')

    def _parse_feed_photos(self, source: dict) -> list:
        return parse_badnamed_dict_list(HornetFeedPhoto, source, 'feed_photos', 'feed_photo')

    def _apicall(func):
        def inner(self, *args, **kwargs):
            t = self.get_current_timeout()
            if t > 0:
                time.sleep(t)

            result = func(self, *args, **kwargs)       
            self._last_apicall_time = time.time()
            return result
        return inner

    # API functions:

    @_apicall
    def get_session(self) -> HornetSession:
        pass

    @_apicall
    def get_location_info(self) -> HornetLocationInfo:
        pass

    @_apicall
    def set_filters(self, min_age: int, max_age: int):
        pass

    @_apicall
    def _get_members(self, path: str, page: int = 1, per_page: int = DEF_MEMBERS_PER_PAGE) -> list:
        pass

    def get_members_near(self, page: int = 1, per_page: int = DEF_MEMBERS_PER_PAGE) -> list:
        return self._get_members(path='near', page=page, per_page=per_page)

    def get_members_recent(self, page: int = 1, per_page: int = DEF_MEMBERS_PER_PAGE) -> list:
        return self._get_members(path='recent', page=page, per_page=per_page)

    def get_members_viewed_me(self, page: int=1, per_page: int= DEF_MEMBERS_PER_PAGE) -> list:
        pass

    @_apicall 
    def get_members_by_username(self, username: str, page: int = 1, per_page: int = 25) -> list:
        pass

    @_apicall
    def get_members_by_hashtags(self, hashtags, page: int = 1, per_page: int = 25) -> list:
        pass

    @_apicall
    def get_member(self, member_id, gallery_preview_photos: int = DEF_GALLERY_PREW_PHOTOS) -> HornetMember:
        pass

    @_apicall
    def get_member_feed_photos(self, member_id, page: int = 1, per_page: int = DEF_MEMBERS_PER_PAGE) -> list:
        pass

    @_apicall
    def get_conversations(self, inbox: str = "primary", page: int = 1, per_page: int = 10) -> HornetConversations:
        pass

    @_apicall
    def get_unread(self, page = 1, per_page: int = 10) -> HornetConversations:
        pass
    
    @_apicall
    def get_requests(self, page = 1, per_page: int = 10) -> HornetConversations:
        pass

    @_apicall
    def get_member_feeds(self, member_id, after = None, per_page: int = 10):
        pass

    @_apicall
    def get_feeds_timeline(self, after = None, per_page: int = 8) -> HornetActivities:
        pass

    @_apicall
    def delete_conversation(self, member_id) -> bool:
        pass

    @_apicall
    def add_ignore_member(self, member_id) -> bool:
        pass

    @_apicall
    def delete_ignore_member(self, member_id) -> bool:
        pass

    @_apicall
    def add_block_member(self, member_id) -> bool:
        pass

    @_apicall
    def delete_block_member(self, member_id) -> bool:
        pass

    @_apicall
    def get_comments(self, activity_id, before = None, after = None) -> HornetComments:
        pass