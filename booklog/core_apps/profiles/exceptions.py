from rest_framework.exceptions import APIException


class AlreadyUseUserNameError(APIException):
    status_code = 400
    default_detail = "Username already used."


class CantFollowYourSelf(APIException):
    status_code = 400
    default_detail = "you can't follow yourself"


class CouldNotFoundProfile(APIException):
    status_code = 400

    def __init__(self, info):
        self.detail = f"`{info}` could not be found into profiles"
