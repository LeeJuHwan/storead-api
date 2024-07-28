from rest_framework.exceptions import APIException


class DuplicateRecommendArticle(APIException):
    status_code = 400
    default_detail = "You have already recommend on this article."


class RecommendationNotFoundException(APIException):
    status_code = 404

    def __init__(self, user, article):
        self.detail = f"Does not found recommendation user: {user}, article: {article}"


class ArticleIdNotFound(APIException):
    status_code = 404
    default_detail = "article_id is not found"
    default_code = "not_found"


class OnlyArticleOwner(APIException):
    status_code = 401
    default_detail = "Only author can retrieve this article"
    default_code = "unauthorized"
