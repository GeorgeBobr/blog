from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from webapp.models import BaseModel

statuses = [("new", "Новая"), ("moderated", "Модерированная"), ("deleted", "Удаленная")]

class Tag(BaseModel):
    name = models.CharField(max_length=31, verbose_name='Тег')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tags"
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"



class Article(BaseModel):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Название")
    content = models.TextField(null=False, blank=False, verbose_name="Контент")
    status = models.CharField(max_length=20, choices=statuses, verbose_name="Статус", default=statuses[0][0])

    author = models.ForeignKey(
        get_user_model(),
        related_name="articles",
        on_delete=models.SET_DEFAULT,
        default=1
    )

    tags = models.ManyToManyField(
        "webapp.Tag",
        related_name="articles",
        verbose_name="Теги",
        blank=True,
        through='webapp.ArticleTag',
        through_fields=("article", "tag"),
    )

    def get_absolute_url(self):
        return reverse("webapp:article_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.pk}. {self.title}: {self.author}"

    class Meta:
        db_table = "articles"
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        permissions = [("change_article_status", "менять статус статье")]

class ArticleTag(BaseModel):
    article = models.ForeignKey('webapp.Article', related_name='tags_articles', on_delete=models.CASCADE, )
    tag = models.ForeignKey('webapp.Tag', related_name='articles_tags', on_delete=models.CASCADE)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        abstract = True

class Comment(BaseModel):
    article = models.ForeignKey('webapp.Article', related_name='comments', on_delete=models.CASCADE,
                                verbose_name='Статья')
    text = models.TextField(max_length=400, verbose_name='Комментарий')

    author = models.ForeignKey(
        get_user_model(),
        related_name="comments",
        on_delete=models.SET_DEFAULT,
        default=1
    )

    def __str__(self):
        return self.text[:20]

    class Meta:
        db_table = "comments"
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"