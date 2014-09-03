import arrow

from mendeley.models.common import Photo
from mendeley.models.profiles import LazyProfile
from mendeley.response import SessionResponseObject, LazyResponseObject


class Group(SessionResponseObject):
    content_type = 'application/vnd.mendeley-group.1+json'

    @property
    def created(self):
        if 'created' in self.json:
            return arrow.get(self.json['created'])
        else:
            return None

    @property
    def photo(self):
        if 'photo' in self.json:
            return Photo(self.json['photo'])
        else:
            return None

    @property
    def owner(self):
        if 'owning_profile_id' in self.json:
            return LazyProfile(self.session, self.json['owning_profile_id'])
        else:
            return None

    @property
    def members(self):
        return self.session.group_members(self.id)

    @property
    def documents(self):
        return self.session.group_documents(self.id)

    @property
    def trash(self):
        return self.session.group_trash(self.id)

    @classmethod
    def fields(cls):
        return ['id', 'name', 'description', 'disciplines', 'tags', 'webpage', 'link', 'access_level',
                'role']


class LazyGroup(LazyResponseObject):
    def __init__(self, session, id):
        super(LazyGroup, self).__init__(session, id, Group)

    def _load(self):
        url = '/groups/%s' % self.id
        rsp = self.session.get(url, headers={'Accept': Group.content_type})

        return rsp.json()


class GroupMember(LazyProfile):
    content_type = 'application/vnd.mendeley-membership.1+json'

    def __init__(self, session, member_json):
        super(GroupMember, self).__init__(session, member_json.get('profile_id'))

        self.member_json = member_json

    @property
    def joined(self):
        if 'joined' in self.member_json:
            return arrow.get(self.member_json['joined'])
        else:
            return None

    @property
    def role(self):
        return self.member_json.get('role')
