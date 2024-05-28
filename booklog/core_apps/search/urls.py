from rest_framework import routers

from .views import ArticleElasticSearchView

router = routers.DefaultRouter(trailing_slash=False)
router.register("/articles", ArticleElasticSearchView, basename="articles")

urlpatterns = router.urls
