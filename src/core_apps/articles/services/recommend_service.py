from core_apps.articles.exceptions import (
    DuplicateRecommendArticle,
    RecommendationNotFoundException,
)
from core_apps.articles.models import Recommend
from core_apps.articles.services.article_query import ArticleQuery
from core_apps.articles.services.recommend_query import RecommendQuery


class RecommendService:
    model = Recommend
    query = RecommendQuery()
    article_query = ArticleQuery()

    def get_recommend(self, user, article):
        try:
            recommend = self.model.objects.get(user=user, article=article)
        except Recommend.DoesNotExist:
            recommend = None

        return recommend

    def create_recommend(self, user, article_id):
        article = self.article_query.get_article(user, article_id)

        if self.query.is_already_recommended(user, article):
            raise DuplicateRecommendArticle()

        recommend = self.model.objects.create(user=user, article=article)
        recommend.save()

        return recommend

    def delete_recommend(self, user, article_id):
        article = self.article_query.get_article(user, article_id)
        recommend = self.get_recommend(user, article)

        if not recommend:
            raise RecommendationNotFoundException(user, article)

        recommend.delete()
