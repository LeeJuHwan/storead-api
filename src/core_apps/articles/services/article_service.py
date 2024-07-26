from typing import Optional

from core_apps.articles.exceptions import ArticleIdNotFound, OnlyArticleOwner
from core_apps.articles.models import Article
from core_apps.articles.serializers.article_serializer import ArticleSerializer
from core_apps.articles.services.article_query import ArticleQuery
from core_apps.articles.services.validators import ArticleValidator
from core_apps.books.models import Book
from core_apps.books.services.book_query import BookQuery


class ArticleService:
    query = ArticleQuery()
    book_query = BookQuery()

    def get_article(self, article_uuid: str):
        return self.query.get_article_by_uuid(article_uuid)

    def update_article(self, article_uuid, author_id, update_data):

        article: Optional[Article] = self.get_article(article_uuid)
        has_perm = ArticleValidator.has_own_permission(article.author.uuid, author_id)

        if not has_perm:
            raise OnlyArticleOwner()
        if not article:
            raise ArticleIdNotFound()

        if "tags" in update_data:
            article.tags.set(update_data["tags"])

        if "book" in update_data:
            book_id = update_data.get("book")
            book: Book = self.book_query.get_book_by_id(book_id)
            article.book = book

        input_serializer = ArticleSerializer(article, data=update_data, partial=True)
        input_serializer.is_valid(raise_exception=True)

        updated_article = input_serializer.save()

        return updated_article

    def delete_article(self, article_uuid: str, author_id: str):
        article = self.get_article(article_uuid)

        has_perm = ArticleValidator.has_own_permission(article.author.uuid, author_id)
        if not has_perm:
            raise ArticleIdNotFound()

        # SoftDelete 추후 적용
        """article.status = ArticleStatus.DELETE"""
        article.delete()
