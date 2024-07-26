from rest_framework.exceptions import APIException


class IncorrectSocialType(APIException):
    status_code = 400
    default_detail = "incorrect social type."


class InvalidAuthorizationCode(APIException):
    status_code = 400
    default_detail = "invalid authorization code"


class DoesNotSupportPlatform(APIException):
    status_code = 400
    default_detail = "does not support social platform"


class PlatformServerException(APIException):
    status_code = 500

    def __init__(self, error, error_description):
        self.detail = {
            "detail": f"error occurred getting access token: {error}, error_description: {error_description}"
        }


class EmptyTokenException(APIException):
    status_code = 400
    default_detail = "token is empty or missing"
