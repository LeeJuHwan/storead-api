from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer
from elasticsearch_dsl.analysis import token_filter

from ..articles.models import Article

nori_analyzer = analyzer(
    "nori_tokenizer",
    tokenizer="nori_tokenizer",
)

custom_edge_ngram_completion = analyzer(
    "edge_ngram_completion",
    tokenizer=nori_analyzer,
    filter=[
        token_filter("edge_ngram_filter_front", type="edge_ngram", min=1, max_gram=10, side="front"),
        token_filter("edge_ngram_filter_back", type="edge_ngram", min=1, max_gram=10, side="back"),
    ],
)


@registry.register_document  # NOTE: Elasticsearch index
class ArticleDocument(Document):
    title = fields.TextField(
        attr="title",
        analyzer=nori_analyzer,
        fields={
            "raw": fields.TextField(),
            "suggest": fields.Completion(),  # NOTE: search to auto complete
            "edge_ngram_completion": fields.TextField(
                analyzer=custom_edge_ngram_completion,
            ),
        },
    )
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
