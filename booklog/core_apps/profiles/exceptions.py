from rest_framework.exceptions import APIException


class EmptyUserNameException(APIException):
    status_code = 400
    default_detail = "username must have input characters"
