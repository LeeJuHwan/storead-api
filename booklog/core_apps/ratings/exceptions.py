from rest_framework.exceptions import APIException


class YouhaveAlreadyRated(APIException):
    status_code = 400
    default_detail = "have already rated this article"
    default_code = "bad_request"


class YouDontHaveRated(APIException):
    status_code = 400
    default_detail = "You have not rated this article yet"
    default_code = "bad_request"


class OnlyAuthorRated(APIException):
    status_code = 401
    default_detail = "Only author can rate this article"
    default_code = "unauthorized"


class ArticleIdNotFound(APIException):
    status_code = 404
    default_detail = "article_id is not found"
    default_code = "not_found"
