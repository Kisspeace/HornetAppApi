from .JsonClass import *
from .ApiTypes import *
from .ClientClass import HornetClientAbs


class HornetClientIter:
    
    def __init__(self, client=None):
        self.client: HornetClientAbs = client

    def __iter__(self):
        return self

    async def __aiter__(self):
        return self


class HornetClientIterPage(HornetClientIter):

    def __init__(self, client=None, start_from=1, per_page=None, stop_at=None):
        super().__init__(client)
        self.page = start_from - 1
        self.stop_at = stop_at
        self.per_page = per_page

    def _client_method(self):
        pass

    def _method_args(self):
        return (self.page, self.per_page)

    def _stop_iteration(self) -> bool:
        if self.stop_at is None:
            return False
        else:
            return (self.page >= self.stop_at)

    def _check_result(self, result) -> bool:
        return True

    def _on_got_result(self, result):
        pass

    def __next__(self):
        if self._stop_iteration():
            raise StopIteration
        self.page += 1
        result = self._client_method()(*self._method_args())
        if (not result) or (not self._check_result(result)):
            raise StopIteration
        self._on_got_result(result)
        return result

    async def __anext__(self):
        if self._stop_iteration():
            raise StopAsyncIteration
        self.page += 1
        result = await self._client_method()(*self._method_args())
        if (not result) or (not self._check_result(result)):
            raise StopAsyncIteration
        self._on_got_result(result)
        return result


class HornetClientIterPagination(HornetClientIterPage):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pagination = HornetPagination()
        self.pagination.next = None
        self.page = 0

    def _on_got_result(self, result):
        self.pagination.next = result.pagination.next
        self.pagination.previous = result.pagination.previous

    def _client_method(self):
        pass

    def _method_args(self):
        return (self.pagination.next, self.per_page)


class HornetClientIterFeedsTimeline(HornetClientIterPagination):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.per_page is None:
            self.per_page = 8

    def _client_method(self):
        return self.client.get_feeds_timeline


class HornetClientMembersPageIter(HornetClientIterPage):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.per_page is None:
            self.per_page = DEF_MEMBERS_PER_PAGE


class HornetClientMembersPageIterNear(HornetClientMembersPageIter):

    def _client_method(self):
        return self.client.get_members_near


class HornetClientMembersPageIterRecent(HornetClientMembersPageIter):

    def _client_method(self):
        return self.client.get_members_recent


class HornetClientMembersPageIterViewedMe(HornetClientMembersPageIter):

    def _client_method(self):
        return self.client.get_members_viewed_me


class HornetClientMembersPageIterByHashtags(HornetClientMembersPageIter):

    def __init__(self, hashtags='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hashtags: str = hashtags

    def _method_args(self):
        return (self.hashtags, self.page, self.per_page)

    def _client_method(self):
        return self.client.get_members_by_hashtags


class HornetClientMembersPageIterByUsername(HornetClientMembersPageIter):

    def __init__(self, username='', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username: str = username

    def _method_args(self):
        return (self.username, self.page, self.per_page)

    def _client_method(self):
        return self.client.get_members_by_username


class HornetClientCommentsPageIter(HornetClientIterPagination):

    def __init__(self, activity_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.activity_id = activity_id

    def _check_result(self, result) -> bool:
        return (result.pagination.previous != '')

    def _client_method(self):
        return self.client.get_comments

    def _method_args(self):
        return (self.activity_id, self.pagination.previous)
