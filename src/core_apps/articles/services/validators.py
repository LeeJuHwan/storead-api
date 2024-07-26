from core_apps.articles.exceptions import OnlyArticleOwner
from core_apps.shared.validator_response import ValidatorResponse


class ArticleValidator:
    response = ValidatorResponse

    def request_user_own_article(self, article_owner, article):
        """
        작성자만 본인이 읽은 책에 대한 평점만 입력 할 수 있다
        """

        if article.author != article_owner:
            return self.response(is_valid=False, error=OnlyArticleOwner)

        return self.response(is_valid=True, data=article)

    @staticmethod
    def has_own_permission(article_author, request_user) -> bool:
        if article_author != request_user:
            return False

        return True
