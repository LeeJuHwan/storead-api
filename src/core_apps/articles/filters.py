import django_filters as filters

from core_apps.articles.models.models import Article


class ArticleFilter(filters.FilterSet):
    author = filters.CharFilter(field_name="author__username", lookup_expr="icontains")
    book = filters.CharFilter(field_name="book__title", lookup_expr="icontains")
    title = filters.CharFilter(field_name="title", lookup_expr="iconatins")
    tags = filters.CharFilter(field_name="tags__name", lookup_expr="iexact")
    created_at = filters.DateFromToRangeFilter(field_name="created_at")
    updated_at = filters.DateFromToRangeFilter(field_name="updated_at")

    class Meta:
        model = Article
        fields = ["author", "title", "tags", "created_at", "updated_at"]
