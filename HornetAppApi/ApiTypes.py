from .JsonClass import * 
from typing import List


API_HOST = "gethornet.com"
API_URL = "https://" + API_HOST + '/api/v3/'
HORNETAPP_URL = 'https://hornetapp.com/'

DEF_MEMBERS_PER_PAGE = 27
DEF_GALLERY_PREW_PHOTOS = 6

class IdAndTitle(JsonLoadable):
    def __init__(self):
        self.id: int = None
        self.title: str = None


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


class HornetComment(JsonLoadable):
    def __init__(self):
        self.id: int = -1
        self.type: str = ''
        self.body: str = ''
        self.profile = HornetPartialMember()
        self.account = self.Account()
        self.owned_by_me: bool = False
        self.created_at: str = None
        self.updated_at: str = None
        self.reactions = HornetReactions() 

    class Account(JsonLoadable):
        def __init__(self):
            self.username: str = ''


class HornetActivity(JsonLoadable): # FIXME not complete yet
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
        self.comments_total: int = 0 # comments: {total: 0}
        self.last_comment: HornetComment = None # comments: {last_comment: null}
        self.awards_total: int = 0 # awards: {total: 0}

    def load_from_dict(self, source: dict):
        JsonLoadable.load_from_dict(self, source)
        # self.reactions_total  = D['reactions']['total']
        # self.reacted_to_by_me = D['reactions']['reacted_to_by_me']
        if 'awards' in source:
            self.awards_total = source['awards']['total']

        if 'comments' in source:
            self.comments_total = source['comments']['total']
            if (('last_comment' in source['comments']) and
                (source['comments']['last_comment'] is not None)):
                self.last_comment = HornetComment()
                self.last_comment.load_from_dict(source['comments']['last_comment'])

        if (('photos' in source) and (self.photos is not None)):
            self.photos = parse_badnamed_dict_list(HornetPartialPhoto, source, 'photos', 'photo')


class HornetActivities(JsonLoadable):
    def __init__(self):
        self.activities: List[HornetActivity] = []
        self.pagination = HornetPagination()

    def load_from_dict(self, source: dict):
        JsonLoadable.load_from_dict(self, source)
        if 'activities' in source:
            self.activities = parse_badnamed_dict_list(HornetActivity, source, 'activities', 'activity')

class HornetComments(JsonLoadable):
    def __init__(self):
        self.comments: List[HornetComment] = []
        self.pagination = HornetPagination()

    def load_from_dict(self, source: dict):
        JsonLoadable.load_from_dict(self, source)
        if 'comments' in source:
            self.comments = parse_badnamed_dict_list(HornetComment, source, 'comments', 'comment')

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
        self.account = self.Account()
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

    class Account(JsonLoadable):
        def __init__(self):
            self.username: str = ''
            self.public: bool = False

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
        self.date_of_birth: str = None
        self.crowned: bool = False
        self.recent_hearts_sent: int = 0
        self.visible: bool = False
        self.show_onboarding: bool = False
        # self.interests = {"hashtags: []"}
        self.created_at: str = ''
        self.relationship = IdAndTitle() # Can be None!
        self.ethnicity = IdAndTitle() # Can be None!
        self.identity = IdAndTitle() # Can be None!
        self.unit_of_measure = IdAndTitle() # Can be None!
        self.gender = IdAndTitle() # Can be None!
        self.sexuality = IdAndTitle() # Can be None!
        self.pronouns = IdAndTitle() # Can be None!
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

    def load_from_dict(self, source: dict):
        HornetPartialMember.load_from_dict(self, source)
        if 'photos' in source:
            self.photos = parse_badnamed_dict_list(HornetPhoto, source, 'photos', 'photo')
          
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

    def load_from_dict(self, source: dict):
        JsonLoadable.load_from_dict(self, source)
        self.chats = parse_badnamed_dict_list(HornetConversation, source, 'conversations', 'conversation') 


class HornetSession(JsonLoadable): # FIXME not complete yet
    def __init__(self):
        self.access_token: str = ''
        self.external_access_token: str = ''
        self.valid_until: str = '' # date
        self.account = self.Account()
        self.profile = HornetMember()
        # self.settings
        self.totals = self.Totals()
        # self.filters
        self.onboarding_objective_set = self.OnboardingObjectiveSet()
        self.public_share_moment_toggle = self.PublicShareMomentToggle()
        self.honey_account = self.HoneyAccount()
        self.hornet_points_account = self.HornetPointsAccount()
        # self.entitlements
        # self.user_video_audience_options

    class Account(JsonLoadable): # FIXME not complete yet
        def __init__(self):
            self.id: int = -1
            self.username: str = ''
            self.sanitized_username: str = ''
            self.username_claimed: bool = False
            self.email: str = ''
            self.email_verified: bool = False
            self.has_password: bool = False
            self.public: bool = False
            self.email_opt_out: bool = False
            self.email_not_deliverable: bool = False
            self.new_user: bool = False
            # self.wallet
            self.premium = self.Premium()
            self.phone_number: any = None
            self.delete_cancelled: bool = False

        class Premium(JsonLoadable):
            def __init__(self):
                self.active: bool = False
                self.subscription: bool = False
                self.valid_until: str = None
                self.premium_plan = None
                self.app_store_identifier = None
                self.cancelled: bool = False

    class Totals(JsonLoadable):
        def __init__(self):
            self.blocks: int = 0
            self.private_photo_access_permissions: int = 0
            self.favourites: int = 0
            self.fans: int = 0
            self.matches: int = 0
            self.posts: int = 0
            self.awards: int = 0
            self.spaces: int = 0
            self.timeline_head: any = None
            self.timeline_updated_at: str = None
            self.notifications_head: any = None
            self.notifications_updated_at: any = None
            self.unread_messages: int = 0
            self.primary_inbox_dot: bool = False
            self.requests_inbox_dot: bool = False

    class OnboardingObjectiveSet(JsonLoadable):
        def __init__(self):
            self.upload_profile_photo: any = None
            self.set_display_name: any = None
            self.follow_member: any = None
            self.post_moment: any = None
            self.updated_at: any = None
            
    class PublicShareMomentToggle(JsonLoadable):
        def __init__(self):
            self.enabled: bool = False
            self.text: str = ''
            self.default_state: bool = False 

    class HoneyAccount(JsonLoadable):
        def __init__(self):
            self.balance: int = 0

    class HornetPointsAccount(JsonLoadable):
        def __init__(self):
            self.id: any = None
            self.balance: int = 0


class HornetLocationInfo(JsonLoadable):
    def __init__(self):
        self.code: str = ''
        self.eu: bool = False

def parse_badnamed_dict_list(item_class, source: list, list_name: str, item_name: str):
    result: List[item_class] = []
    for obj in source[list_name]:
        item = item_class()
        item.load_from_dict(obj[item_name])
        result.append(item)
    return result
