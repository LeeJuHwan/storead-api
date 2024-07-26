from core_apps.ratings.exceptions import RatingDoesNotExist
from core_apps.ratings.models import Rating
from core_apps.ratings.services.rating_validator import RatingValidator
from core_apps.shared.base.selectors import BaseSelector


class RatinQuery(BaseSelector):
    validator = RatingValidator()

    def _is_exists_rate_on_article(self, user, article_id):
        query_result = Rating.objects.filter(user=user, article__id=article_id).exists()
        return query_result

    def get_rating_select_related(self, request_user, article_id):
        try:
            return Rating.objects.select_related("article").get(user=request_user, article__id=article_id)
        except Rating.DoesNotExist:
            raise RatingDoesNotExist

    def get_exists_rate_on_article(self, user_id, article_id):
        query_result = self._is_exists_rate_on_article(user_id, article_id)
        rating_valid = self.validator.already_user_rated(query_result)
        return self._response(rating_valid)

    def get_not_exists_rate_on_article(self, user_id, article_id):
        query_result = self._is_exists_rate_on_article(user_id, article_id)
        rating_valid = self.validator.dont_have_rated(query_result)
        return self._response(rating_valid)
