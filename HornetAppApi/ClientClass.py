import time
from .JsonClass import *
from .ApiTypes import *

class HornetClientAbs:
    def __init__(self):
        self.ApiCallTimeout = 0.380 # 380 ms. set 0 to disable
        # self.LastResponse = None
        # public events
        self.OnResponse = None # reference to procedure (sender: HornetClientAbs, response)
        # protected
        self._LastApiCallTime = None
    
    # Setters & getters:

    def SetHeaders(self, headers):
        pass

    def GetHeaders(self) -> dict:
        pass

    def SetToken(self, token: str):
        pass

    def GetToken(self) -> str:
        pass

    def GetCurrentTimeout(self) -> float:
        result = 0
        if ((self._LastApiCallTime != None) and (self.ApiCallTimeout > 0)):
            t = (time.time() - self._LastApiCallTime)
            if (t < self.ApiCallTimeout):
                result =  (self.ApiCallTimeout - t)    
        else:
            result = 0
        return result

    # protected

    def _DoOnResponse(self, response):
        if callable(self.OnResponse):
            self.OnResponse(self, response)

    def _ParseMembers(self, D) -> list:
        return ParseBadNamedDictList(HornetPartialMember, D, 'members', 'member')

    def _ApiCall(func):
        def inner(self, *args, **kwargs):
            t = self.GetCurrentTimeout()
            if (t > 0):
                # print('sleep: ', t)
                time.sleep(t)
            
            result = func(self, *args, **kwargs)       
            self._LastApiCallTime = time.time()
            # print(f'{func.__name__} finished at: {self._LastApiCallTime}')
            return result
        return inner

    # API functions:

    @_ApiCall
    def SetFilters(self, minAge, maxAge):
        pass

    @_ApiCall
    def _GetMembers(self, path: str, page = 1, perPage = DEF_MEMBERS_PER_PAGE) -> list:
        pass

    def GetMembersNear(self, page = 1, perPage = DEF_MEMBERS_PER_PAGE) -> list:
        return self._GetMembers(path='near', page=page, perPage=perPage)

    def GetMembersRecent(self, page = 1, perPage = DEF_MEMBERS_PER_PAGE) -> list:
        return self._GetMembers(path='recent', page=page, perPage=perPage)
     
    @_ApiCall 
    def GetMembersByUsername(self, username: str, page = 1, perPage = 25) -> list:
        pass
    
    @_ApiCall
    def GetMembersByHashtags(self, hashtags, page = 1, perPage = 25) -> list:
        pass

    @_ApiCall
    def GetMember(self, id, gallery_preview_photos = DEF_GALLERY_PREW_PHOTOS) -> HornetMember:
        pass

    @_ApiCall
    def GetMemberFeedPhotos(self, memberId, page = 1, perPage = DEF_MEMBERS_PER_PAGE) -> list:
        pass

    @_ApiCall
    def GetConversations(self, inbox = "primary", page = 1, perPage = 10) -> HornetConversations:
        pass

    @_ApiCall
    def GetUnread(self, page = 1, perPage = 10) -> HornetConversations:
        pass

    @_ApiCall
    def GetMemberFeeds(self, memberId, after = None, perPage = 10):
        pass

    @_ApiCall
    def GetFeedsTimeline(self, after = None, perPage = 8) -> HornetActivities:
        pass

    @_ApiCall
    def DeleteConversation(self, memberId) -> bool:
        pass

    

        