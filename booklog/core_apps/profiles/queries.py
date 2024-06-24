from core_apps.profiles.exceptions import CouldNotFoundProfile
from core_apps.profiles.models import Profile
from django.utils.functional import classproperty


class ProfileQuery:

    @classproperty
    def select_related(self):
        return Profile.objects.select_related("user").all()

    @staticmethod
    def get_profile_by_user(user):
        try:
            return ProfileQuery.select_related.get(user=user)
        except Profile.DoesNotExist:
            raise CouldNotFoundProfile(user)

    @staticmethod
    def get_profile_by_user_uuid(uuid):
        try:
            return ProfileQuery.select_related.get(user__uuid=uuid)
        except Profile.DoesNotExist:
            raise CouldNotFoundProfile(uuid)

    @staticmethod
    def get_profile_by_profile_id(profile_id):
        try:
            return Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            raise CouldNotFoundProfile(profile_id)
