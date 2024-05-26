from rest_framework import serializers

from ..articles.models import Article, ArticleView, Recommend
from ..books.excpetions import BookNotFound
from ..books.models import Book
from ..books.serializers import BookListSerializer
from ..comments.serializers import CommentSerializer
from ..profiles.serializers import ProfileSerializer


class TagListField(serializers.Field):
    def to_representation(self, value):
        return [tag.name for tag in value.all()]

    def to_internal_value(self, data):
        if not isinstance(data, list):
            raise serializers.ValidationError("Expected a list of tags")

        tag_objects = [tag_name.strip() for tag_name in data if tag_name]
        return tag_objects


class ArticleSerializer(serializers.ModelSerializer):
    author_info = ProfileSerializer(source="author.profile", read_only=True)
    book = BookListSerializer(read_only=True)
    estimated_reading_time = serializers.ReadOnlyField()
    tags = TagListField()
    views = serializers.SerializerMethodField()
    recommend_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    author_rating = serializers.ReadOnlyField()

    def get_views(self, obj):
        return ArticleView.objects.filter(article=obj).count()

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
        print(f"create validate data: {validated_data}")
        tags = validated_data.pop("tags")
        article = Article.objects.create(**validated_data)
        article.tags.set(tags)

        # TODO: select query 분리
        if book_uuid := self.context["request"].data.get("book"):
            try:
                book = Book.objects.get(id=book_uuid)
                article.book = book
                article.save()
            except Book.DoesNotExist:
                raise BookNotFound

        return article

    def update(self, instance, validated_data):
        instance.author = validated_data.get("author", instance.author)
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.body = validated_data.get("body", instance.body)
        instance.updated_at = validated_data.get("updated_at", instance.updated_at)

        # TODO: select query 분리
        if book_uuid := self.context["request"].data.get("book"):
            try:
                book = Book.objects.get(id=book_uuid)
                instance.book = book
            except Book.DoesNotExist:
                raise BookNotFound

        if "tags" in validated_data:
            instance.tags.set(validated_data["tags"])

        instance.save()
        return instance

    class Meta:
        model = Article
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
        model = Recommend
        fields = ["id", "user_name", "article_title"]
