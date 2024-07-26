from rest_framework import serializers

from core_apps.articles.models import article_model, recommend_model
from core_apps.books.excpetions import BookHasEmpty, BookNotFound
from core_apps.books.models import Book
from core_apps.books.serializers.book_serializer import BookListSerializer
from core_apps.comments.serializers.comment_serializer import CommentSerializer
from core_apps.profiles.serializers import ProfileSerializer


class TagListField(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, list):
            return value
        return [tag.name for tag in value.all()]

    def to_internal_value(self, data):
        if not isinstance(data, list):
            raise serializers.ValidationError("Expected a list of tags")

        tag_objects = [tag_name.strip() for tag_name in data if tag_name]
        print(f"tag objects: {tag_objects}")
        return tag_objects


class ArticleSerializer(serializers.ModelSerializer):
    author_info = ProfileSerializer(source="author.profile", read_only=True)
    book = BookListSerializer(read_only=True)
    estimated_reading_time = serializers.ReadOnlyField()
    tags = TagListField()
    slug = serializers.CharField(read_only=True)
    views = serializers.SerializerMethodField()
    recommend_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    author_rating = serializers.ReadOnlyField()

    def get_views(self, obj):
        return article_model.ArticleView.objects.filter(article=obj).count()

    def get_recommend_count(self, obj):
        return obj.recommends.count()

    def get_created_at(self, obj):
        now = obj.created_at
        formatted_date = now.strftime("%Y/%m/%d, %H:%M:%S")
        return formatted_date

    def get_updated_at(self, obj):
        then = obj.updated_at
        formatted_date = then.strftime("%Y/%m/%d, %H:%M:%S")
        return formatted_date

    def get_author_rating(self, obj):
        return obj.author_rating()

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        book = None

        if book_uuid := self.context["request"].data.get("book"):
            try:
                book = Book.objects.get(id=book_uuid)
            except Book.DoesNotExist:
                raise BookNotFound()

        if not book:
            raise BookHasEmpty()

        validated_data["book"] = book
        article = article_model.Article.objects.create(**validated_data)
        article.tags.set(tags)

        article.book = book
        article.save()
        return article

    class Meta:
        model = article_model.Article
        fields = [
            "id",
            "book",
            "title",
            "slug",
            "tags",
            "estimated_reading_time",
            "author_info",
            "views",
            "description",
            "body",
            "created_at",
            "updated_at",
            "recommend_count",
            "comments",
            "comments_count",
            "author_rating",
        ]


class RecommendSerializer(serializers.ModelSerializer):
    article_title = serializers.CharField(source="article.title", read_only=True)
    user_name = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = recommend_model.Recommend
        fields = ["id", "user_name", "article_title"]
