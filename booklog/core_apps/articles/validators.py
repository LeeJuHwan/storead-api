from core_apps.common.validator_response import ValidatorResponse

from .exceptions import OnlyArticleOwner


class ArticleValidator:
    response = ValidatorResponse

    def request_user_own_article(self, article_owner, article):
        """
        작성자만 본인이 읽은 책에 대한 평점만 입력 할 수 있다
        """

        if article.author != article_owner:
            return self.response(is_valid=False, error=OnlyArticleOwner)

        return self.response(is_valid=True, data=article)
