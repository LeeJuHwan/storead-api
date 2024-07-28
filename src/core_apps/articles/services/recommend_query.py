from core_apps.articles.models import Recommend


class RecommendQuery:
    model = Recommend

    def is_already_recommended(self, user, article):
        if self.model.objects.filter(user=user, article=article).exists():
            return True
        return False
