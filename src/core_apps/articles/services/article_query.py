from typing import Optional

from django.db.models import QuerySet

from core_apps.articles.exceptions import ArticleIdNotFound
from core_apps.articles.models import Article
from core_apps.articles.services.validators import ArticleValidator
from core_apps.shared.base.selectors import BaseSelector


class ArticleQuery(BaseSelector):
    validator = ArticleValidator()

    def get_article(self, request_user, article_id):
        try:
            article: QuerySet = Article.objects.get(id=article_id)
            article_valid = self.validator.request_user_own_article(request_user, article)
            return self._response(article_valid)

        except Article.DoesNotExist:
            raise ArticleIdNotFound

    @staticmethod
    def get_article_by_uuid(article_id: str) -> Optional[Article]:
        """
        UUID로 게시글 조회
        """
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            article = None

        return article
