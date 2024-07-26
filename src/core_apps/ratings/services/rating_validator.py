from core_apps.ratings.exceptions import YouDontHaveRated, YouHaveAlreadyRated
from core_apps.shared.validator_response import ValidatorResponse


class RatingValidator:
    response = ValidatorResponse

    def already_user_rated(self, is_exists_article: bool) -> ValidatorResponse:
        if is_exists_article:
            return self.response(is_valid=False, error=YouHaveAlreadyRated)
        return self.response(is_valid=True, data=is_exists_article)

    def dont_have_rated(self, is_exists_article: bool) -> ValidatorResponse:
        if not is_exists_article:
            return self.response(is_valid=False, error=YouDontHaveRated)
        return self.response(is_valid=True, data=is_exists_article)
