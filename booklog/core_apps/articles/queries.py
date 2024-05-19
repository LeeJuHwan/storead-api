from core_apps.common.base.selectors import BaseSelector

from .exceptions import ArticleIdNotFound
from .models import Article
from .validators import ArticleValidator


class ArticleSelector(BaseSelector):
    validator = ArticleValidator()

    def get_article(self, request_user, article_id):
        try:
            article = Article.objects.get(id=article_id)
            article_valid = self.validator.request_user_own_article(request_user, article)
            return self._response(article_valid)

        except Article.DoesNotExist:
            raise ArticleIdNotFound
