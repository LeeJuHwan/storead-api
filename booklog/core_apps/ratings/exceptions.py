from rest_framework.exceptions import APIException


class YouHaveAlreadyRated(APIException):
    status_code = 400
    default_detail = "have already rated this article"
    default_code = "bad_request"


class YouDontHaveRated(APIException):
    status_code = 400
    default_detail = "You have not rated this article yet"
    default_code = "bad_request"


class RatingDoesNotExist(APIException):
    status_code = 404
    default_detail = "Rating does not exist"
    default_code = "not_found"
