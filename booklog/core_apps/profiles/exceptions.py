from rest_framework.exceptions import APIException


class EmptyUserNameException(APIException):
    status_code = 400
    default_detail = "username must have input characters"


class CantFollowYourSelf(APIException):
    status_code = 400
    default_detail = "you can't follow yourself"


class CantUnfollowNotFollowingUser(APIException):
    status_code = 400

    def __init__(self, username):
        self.detail = {
            "detail": f"you can't unfollow {username}, since you were not following then in the first place"
        }


class AlreadyFollowing(APIException):
    status_code = 400

    def __init__(self, username):
        self.detail = {
            "detail": f"you are already following {username}"
        }
