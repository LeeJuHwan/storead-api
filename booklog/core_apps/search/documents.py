from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer

from ..articles.models import Article

nori_analyzer = analyzer(
    "nori_tokenizer",
    tokenizer="nori_tokenizer",
)


@registry.register_document  # NOTE: Elasticsearch index
class ArticleDocument(Document):
    title = fields.TextField(attr="title", analyzer=nori_analyzer)
    description = fields.TextField(attr="description", analyzer=nori_analyzer)
    body = fields.TextField(attr="body", analyzer=nori_analyzer)
    author_username = fields.TextField()
    tags = fields.KeywordField()
    book_title = fields.TextField(analyzer=nori_analyzer)

    class Index:
        name = "articles"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:  # NOTE: 모델 소스 정의
        model = Article
        fields = ["created_at"]

    # NOTE: 인덱싱 필드 정의
    def prepare_book_title(self, instance):
        return instance.book.title

    def prepare_author_username(self, instance):
        return instance.author.username

    def prepare_tags(self, instance):
        return [tag.name for tag in instance.tags.all()]
