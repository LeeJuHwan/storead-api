from core_apps.articles.services.article_query import ArticleQuery
from core_apps.ratings.models import Rating
from core_apps.ratings.serializers.rating_serializer import RatingSerializer
from core_apps.ratings.services.rating_query import RatinQuery


class RatingService:
    _query = RatinQuery()
    _article_query = ArticleQuery()

    def create_rating(self, article_id, user, validated_data):
        article = self._article_query.get_article(user, article_id)
        self._query.get_exists_rate_on_article(user, article_id)  # NOTE: Validation

        validated_data["article"] = article
        validated_data["user"] = user
        return Rating.objects.create(**validated_data)

    def update_rating(self, article_id, user, validated_data):
        self._article_query.get_article(user, article_id)
        rating = self._query.get_rating_select_related(user, article_id)
        self._query.get_not_exists_rate_on_article(user, article_id)  # NOTE: Validation

        input_serializer = RatingSerializer(rating, data=validated_data, partial=True)
        input_serializer.is_valid(raise_exception=True)
        return input_serializer.save()
