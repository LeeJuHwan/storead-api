from rest_framework.exceptions import APIException


class BookNotFound(APIException):
    status_code = 404
    default_detail = "Does not exist book"
    default_code = "not_found"
