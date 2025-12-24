from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Article, ArticleSlugHistory

@receiver(pre_save, sender=Article)
def article_slig_update(sender, instance, **kwargs):
    if instance.pk:
        old_article = Article.objects.get(pk = instance.pk)

        if old_article.title != instance.title:
            ArticleSlugHistory.objects.create(
                article = instance,
                old_slug = old_article.slug
            )
            base_slug = slugify(instance.title)
            slug = base_slug
            count = 1

            while Article.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1

            instance.slug = slug
    else:     
        base_slug = slugify(instance.title)
        slug = base_slug
        count = 1

        while Article.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1

        instance.slug = slug
