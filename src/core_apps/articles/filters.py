import django_filters as filters

from core_apps.articles.models import Article


class ArticleFilter(filters.FilterSet):
    tags = filters.CharFilter(field_name="tags__name", lookup_expr="iexact")

    class Meta:
        model = Article
        fields = ["tags"]
