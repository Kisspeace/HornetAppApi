from .JsonClass import * 

API_HOST = "gethornet.com"
API_URL = "https://" + API_HOST + '/api/v3/' # "/api/v3/members/near?page=1&per_page=27"

DEF_MEMBERS_PER_PAGE = 27
DEF_GALLERY_PREW_PHOTOS = 6

class IdAndTitle(JsonLoadable):
    def __init__(self):
        self.id = -1
        self.title = ''

class HornetPagination(JsonLoadable):
    def __init__(self):
        self.previous = None
        self.next = None

class HornetFeedPhoto(JsonLoadable):
    def __init__(self):
        self.id = -1
        self.state = ''
        self.url = ""
        self.full_large_url = ""
        self.thumbnail_large_url = ""
        self.square_url = ""
        self.activity_id = -1

class HornetReactions(JsonLoadable):
    def __init__(self):
        self.total = 0
        self.reacted_to_by_me = False

class HornetPartialComment(JsonLoadable):
    def __init__(self):
        self.id = -1
        self.type = ''
        self.body = ''
        self.profile = HornetPartialMember()
        self.account_username = '' # account: {username: ''}
        self.owned_by_me = False
        self.created_at = None
        self.updated_at = None
        self.reactions = HornetReactions() 

    def LoadFromDict(self, D):
        JsonLoadable.LoadFromDict(self, D)
        self.account_username = D['account']['username']

class HornetActivity(JsonLoadable):
    def __init__(self):
        self.id	= -1
        self.title = ''
        self.body = ''
        self.action = ''
        # self.activity_metadata = None
        self.owned_by_me = False
        self.created_at = ""
        self.activity_type = ""
        # bottom_heading	null
        # carousel_style	null
        # activity_analytics	{…}
        # top_right_nav_action	null
        # top_right_nav_text	null
        self.accepts_reports = True
        self.accepts_reactions = True
        self.accepts_comments = True
        self.accepts_ignores = False
        self.accepts_shares	= False
        self.accepts_awards = True
        self.is_muteable = False
        self.is_muted = False
        self.photos = [] # List of HornetPartialPhoto
        self.profile = HornetPartialMember()
        # thumbnail	{…}
        self.reactions = HornetReactions()
        # self.reactions_total = 0 # reactions: {total: 0} 
        # self.reacted_to_by_me = False # reactions: {reacted_to_by_me: false} 
        self.comments_total = 0 # comments: {total: 0} 
        self.last_comment = None # comments: {last_comment: null} 
        self.awards_total = 0 # awards: {total: 0}

    def LoadFromDict(self, D):
        JsonLoadable.LoadFromDict(self, D)
        # self.reactions_total  = D['reactions']['total']
        # self.reacted_to_by_me = D['reactions']['reacted_to_by_me']
        if ('awards' in D):
            self.awards_total = D['awards']['total']

        if ('comments' in D):
            self.comments_total = D['comments']['total']
            if (('last_comment' in D['comments']) and (D['comments']['last_comment'] != None)): #FIXME
                self.last_comment = HornetPartialComment()
                self.last_comment.LoadFromDict(D['comments']['last_comment'])

        if (('photos' in D) and (self.photos != None)):
            self.photos = ParseBadNamedDictList(HornetPartialPhoto, D, 'photos', 'photo')

class HornetActivities(JsonLoadable):
    def __init__(self):
        self.activities = []
        self.pagination = HornetPagination()
    
    def LoadFromDict(self, D):
        JsonLoadable.LoadFromDict(self, D)
        if ('activities' in D):
            self.activities = ParseBadNamedDictList(HornetActivity, D, 'activities', 'activity')

class HornetPartialPhoto(JsonLoadable):
    def __init__(self):
        self.full_large_url = ""
        self.thumbnail_url = ""
        self.thumbnail_large_url = ""
        self.square_url = ""

class HornetPhoto(HornetPartialPhoto):
    def __init__(self):
        HornetPartialPhoto.__init__(self)
        self.id = -1
        self.state = ""
        self.slot = 0
        self.is_public = False
        self.is_primary = False
        self.url = ""
        self.full_url = ""
        self.v6_full_url = ""  

class HornetPartialMember(JsonLoadable):   
    def __init__(self):
        self.id           = -1
        self.display_name = ''
        self.mitch_rank_index = None
        self.age          = -1
        # self.account": {"username": "fffff0", "public": true}
        self.account_username = ''
        self.account_public   = False
        self.distance         = 0.0
        self.unread_messages_from = 0
        self.explorer = False
        self.online   = False
        self.status_icon = ''
        self.last_online = None
        self.favourite = False
        self.fan       = False
        self.system_profile = False
        self.broadcast_profile = False
        self.verification_level = -1
        self.public_user_video_feed_entry_id = None
        self.broadcast_started_at = None
        self.vpaas_id = None
        self.thumbnail_url           = ''
        self.thumbnail_large_url     = ''
        self.profile_photo_url       = ''
        self.profile_photo_large_url = ''
        self.square_url              = ''
        self.v6_full_url             = ''

    def LoadFromDict(self, D):
        JsonLoadable.LoadFromDict(self, D)
        if ('account' in D):
            self.account_username     = D['account']['username']
            self.account_public       = D['account']['public']

    def IsValid(self):
        return (self.id != -1)

    def HasAvatar(self):
        return (self.profile_photo_url != "")

class HornetMember(HornetPartialMember):
    def __init__(self):
        HornetPartialMember.__init__(self)
        self.headline = ""
        self.about_you = ""
        self.height = None
        self.weight = None
        self.show_distance = False
        self.preferred_language = ""
        self.location = None
        self.bio = "" # is about_you ???
        self.crowned = False
        self.recent_hearts_sent = 0
        self.visible = False
        self.show_onboarding = False
        # self.interests = {"hashtags: []"}
        self.created_at = ""
        self.relationship_id = -1 # relationship 
        self.relationship_title = ""
        self.ethnicity = None
        self.identity = None
        self.unit_of_measure_id = -1
        self.unit_of_measure_title = ""
        self.gender = None
        self.sexuality = None
        self.pronouns = None
        # self.looking_fors = {"looking_fors": []}
        self.public = None
        self.private = None
        self.city = None
        self.photos = [] # List of HornetPhoto
        self.private_photos_accessible = False
        self.msgs = 0
        self.note = ""
        self.private_photo_access = None
        self.my_private_photos_access = None
        self.spaces_count = 0
        # self.followers = []
        self.followers_count = 0
        self.followed_count = 0
        self.posts_count = 0

    def LoadFromDict(self, D):
        HornetPartialMember.LoadFromDict(self, D)
        self.unit_of_measure_id    = D['unit_of_measure']['id']
        self.unit_of_measure_title = D['unit_of_measure']['title']

        if ( 'photos' in D ):
            self.photos = ParseBadNamedDictList(HornetPhoto, D, 'photos', 'photo')
    
    def HasAvatar(self):
        return (len(self.photos) > 0)

class HornetPartialMessage(JsonLoadable):
    def __init__(self):
        self.created_at = None
        self.state = ""
        self.data = ""
        self.type = ""

class HornetConversation(JsonLoadable):
    def __init__(self):
        self.profile = HornetPartialMember()
        self.last_message = HornetPartialMessage()

class HornetConversations(JsonLoadable):
    def __init__(self):
        self.chats = []
        self.unread_count = -1
        self.inbox = ''

    def LoadFromDict(self, D):
        JsonLoadable.LoadFromDict(self, D)
        self.chats = ParseBadNamedDictList(HornetConversation, D, 'conversations', 'conversation') 







def ParseBadNamedDictList(itemClass, d, listName, itemName):
    Result = []
    for obj in d[listName]:
        item = itemClass()
        item.LoadFromDict(obj[itemName])
        Result.append(item)
    return Result  
