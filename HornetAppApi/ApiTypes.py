from .JsonClass import * 
from typing import List

API_HOST = "gethornet.com"
API_URL = "https://" + API_HOST + '/api/v3/' # "/api/v3/members/near?page=1&per_page=27"

DEF_MEMBERS_PER_PAGE = 27
DEF_GALLERY_PREW_PHOTOS = 6

class IdAndTitle(JsonLoadable):
    def __init__(self):
        self.id: int = -1
        self.title: str = ''

class HornetPagination(JsonLoadable):
    def __init__(self):
        self.previous = None
        self.next = None

class HornetFeedPhoto(JsonLoadable):
    def __init__(self):
        self.id: int = -1
        self.state = ''
        self.url: str = ""
        self.full_large_url: str = ""
        self.thumbnail_large_url: str = ""
        self.square_url: str = ""
        self.activity_id: int = -1

class HornetReactions(JsonLoadable):
    def __init__(self):
        self.total: int = 0
        self.reacted_to_by_me: bool = False

class HornetPartialComment(JsonLoadable):
    def __init__(self):
        self.id: int = -1
        self.type: str = ''
        self.body: str = ''
        self.profile = HornetPartialMember()
        self.account_username: str = '' # account: {username: ''}
        self.owned_by_me: bool = False
        self.created_at: str = None
        self.updated_at: str = None
        self.reactions = HornetReactions() 

    def LoadFromDict(self, D):
        JsonLoadable.LoadFromDict(self, D)
        self.account_username = D['account']['username']

class HornetActivity(JsonLoadable):
    def __init__(self):
        self.id: int = -1
        self.title: str = ''
        self.body: str = ''
        self.action: str = ''
        # self.activity_metadata = None
        self.owned_by_me: bool = False
        self.created_at: str = ""
        self.activity_type: str = ""
        # bottom_heading	null
        # carousel_style	null
        # activity_analytics	{…}
        # top_right_nav_action	null
        # top_right_nav_text	null
        self.accepts_reports: bool = True
        self.accepts_reactions: bool = True
        self.accepts_comments: bool = True
        self.accepts_ignores: bool = False
        self.accepts_shares: bool	= False
        self.accepts_awards: bool = True
        self.is_muteable: bool = False
        self.is_muted: bool = False
        self.photos: List[HornetPartialPhoto] = []# List of HornetPartialPhoto
        self.profile = HornetPartialMember()
        # thumbnail	{…}
        self.reactions = HornetReactions()
        # self.reactions_total = 0 # reactions: {total: 0}
        # self.reacted_to_by_me = False # reactions: {reacted_to_by_me: false}
        self.comments_total: int = 0 # comments: {total: 0}
        self.last_comment: any = None # comments: {last_comment: null}
        self.awards_total: int = 0 # awards: {total: 0}

    def LoadFromDict(self, D):
        JsonLoadable.LoadFromDict(self, D)
        # self.reactions_total  = D['reactions']['total']
        # self.reacted_to_by_me = D['reactions']['reacted_to_by_me']
        if 'awards' in D:
            self.awards_total = D['awards']['total']

        if 'comments' in D:
            self.comments_total = D['comments']['total']
            if (('last_comment' in D['comments']) and
                (D['comments']['last_comment'] is not None)):
                self.last_comment = HornetPartialComment()
                self.last_comment.LoadFromDict(D['comments']['last_comment'])

        if (('photos' in D) and (self.photos is not None)):
            self.photos = ParseBadNamedDictList(HornetPartialPhoto, D, 'photos', 'photo')

class HornetActivities(JsonLoadable):
    def __init__(self):
        self.activities: List[HornetActivity] = []
        self.pagination = HornetPagination()
        
    def LoadFromDict(self, D):
        JsonLoadable.LoadFromDict(self, D)
        if 'activities' in D:
            self.activities = ParseBadNamedDictList(HornetActivity, D, 'activities', 'activity')

class HornetPartialPhoto(JsonLoadable):
    def __init__(self):
        self.full_large_url: str = ""
        self.thumbnail_url: str = ""
        self.thumbnail_large_url: str = ""
        self.square_url: str = ""

class HornetPhoto(HornetPartialPhoto):
    def __init__(self):
        HornetPartialPhoto.__init__(self)
        self.id: int = -1
        self.state: str = ""
        self.slot: int = 0
        self.is_public: bool = False
        self.is_primary: bool = False
        self.url: str = ""
        self.full_url: str = ""
        self.v6_full_url: str = ""  

class HornetPartialMember(JsonLoadable):  
    def __init__(self):
        self.id: int = -1
        self.display_name: str = ''
        self.mitch_rank_index = None
        self.age: int = None
        # self.account": {"username": "fffff0", "public": true}
        self.account_username: str = ''
        self.account_public: bool = False
        self.distance: float = 0.0
        self.unread_messages_from: int = 0
        self.explorer: bool = False
        self.online: bool = False
        self.status_icon: str = ''
        self.last_online: str = None
        self.favourite: bool = False
        self.fan: bool = False
        self.system_profile: bool = False
        self.broadcast_profile: bool = False
        self.verification_level: int = -1
        self.public_user_video_feed_entry_id: int = None
        self.broadcast_started_at: str = None
        self.vpaas_id: any = None
        self.thumbnail_url: str = ''
        self.thumbnail_large_url: str = ''
        self.profile_photo_url: str = ''
        self.profile_photo_large_url: str = ''
        self.square_url: str = ''
        self.v6_full_url: str= ''

    def LoadFromDict(self, D):
        JsonLoadable.LoadFromDict(self, D)
        if 'account' in D:
            self.account_username = D['account']['username']
            self.account_public   = D['account']['public']

    def IsValid(self):
        return self.id != -1

    def HasAvatar(self):
        return self.profile_photo_url != ""

class HornetMember(HornetPartialMember):
    def __init__(self):
        HornetPartialMember.__init__(self)
        self.headline: str = ''
        self.about_you: str = ''
        self.height: int = None
        self.weight: int = None
        self.show_distance: bool = False
        self.preferred_language: str = ''
        self.location: str = None
        self.bio: str = '' # is about_you ???
        self.crowned: bool = False
        self.recent_hearts_sent: int = 0
        self.visible: bool = False
        self.show_onboarding: bool = False
        # self.interests = {"hashtags: []"}
        self.created_at: str = ''
        self.relationship = IdAndTitle()
        self.ethnicity = IdAndTitle()
        self.identity = IdAndTitle()
        self.unit_of_measure = IdAndTitle()
        self.gender = IdAndTitle()
        self.sexuality = IdAndTitle()
        self.pronouns = IdAndTitle()
        # self.looking_fors = {"looking_fors": []}
        self.public: int = None # public photos count
        self.private: int = None # private photos count
        self.city: str = None
        self.photos: List[HornetPhoto] = [] # List of HornetPhoto
        self.private_photos_accessible: bool = False
        self.msgs: int = 0
        self.note: str = ''
        self.private_photo_access: bool = None
        self.my_private_photos_access: bool = None
        self.spaces_count: int = 0
        # self.followers = []
        self.followers_count: int = 0
        self.followed_count: int = 0
        self.posts_count: int = 0

    def LoadFromDict(self, D):
        HornetPartialMember.LoadFromDict(self, D)
        if 'photos' in D:
            self.photos = ParseBadNamedDictList(HornetPhoto, D, 'photos', 'photo')
            
    def HasAvatar(self):
        return len(self.photos) > 0

class HornetPartialMessage(JsonLoadable):
    def __init__(self):
        self.created_at: str = None
        self.state: str = ''
        self.data: str = ''
        self.type: str = '' #FIXME maybe int

class HornetConversation(JsonLoadable):
    def __init__(self):
        self.profile = HornetPartialMember()
        self.last_message = HornetPartialMessage()

class HornetConversations(JsonLoadable):
    def __init__(self):
        self.chats: List[HornetConversation] = []
        self.unread_count: int = -1
        self.inbox: str = '' # inbox type

    def LoadFromDict(self, D):
        JsonLoadable.LoadFromDict(self, D)
        self.chats = ParseBadNamedDictList(HornetConversation, D, 'conversations', 'conversation') 







def ParseBadNamedDictList(itemClass, d, listName, itemName):
    Result: List[itemClass] = []
    print(type(Result))
    for obj in d[listName]:
        item = itemClass()
        item.LoadFromDict(obj[itemName])
        Result.append(item)
    return Result  
