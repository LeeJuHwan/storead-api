# Generated by Django 4.2.11 on 2024-07-18 23:03
import random

from django.db import migrations
from django.utils.text import slugify

from utils.common.unique_slugify import generate_unique_slugify


def create_dummy_articles(apps, schema_editor):
    Article = apps.get_model("articles", "Article")

    adv = ["진짜", "정말", "매우"]
    adj = ["재밌는", "어려운", "쉬운"]
    lang = ["자바", "파이썬", "고"]

    for _ in range(50):
        to_create = []
        for num, _ in enumerate(range(2000)):
            title = random.choice(adv) + random.choice(adj) + random.choice(lang)
            description = f"{title} 테스트 아티클"
            body = f"{description} 본문"
            slug = slugify(title, allow_unicode=True)
            gen_slug = generate_unique_slugify(Article, slug) + str(num) + str(random.randint(1, 10000000))
            to_create.append(Article(title=title, description=description, slug=gen_slug, body=body, author_id=1))

        Article.objects.bulk_create(to_create)


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_article_article_title_gin_index'),
    ]

    operations = [
        migrations.RunPython(create_dummy_articles, reverse_code=migrations.RunPython.noop),
    ]
