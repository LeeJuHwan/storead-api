from rest_framework.exceptions import APIException


class DuplicateRecommendArticle(APIException):
    status_code = 400
    default_detail = "You have already recommend on this article."
