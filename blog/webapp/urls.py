from django.urls import path
from django.views.generic import RedirectView

from webapp.views.like import LikeToggleView
from webapp.views.views import UpdateArticleView, DeleteArticleView, ArticleListView, CreateArticleView, \
    ArticleDetailView
from webapp.views.second_views import UpdateCommentView, DeleteCommentView, CreateCommentView
from webapp.views.views import TestJsView

app_name = 'webapp'

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('', RedirectView.as_view(pattern_name='webapp:articles')),
    path('create/', CreateArticleView.as_view(), name='create_article'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article/<int:pk>/update/', UpdateArticleView.as_view(), name='update_article'),
    path('article/<int:pk>/delete/', DeleteArticleView.as_view(), name='delete_article'),

    path('article/<int:pk>/comment/create/', CreateCommentView.as_view(), name='create_comment'),
    path('comment/<int:pk>/update/', UpdateCommentView.as_view(), name='update_comment'),
    path('comment/<int:pk>/delete/', DeleteCommentView.as_view(), name='delete_comment'),

    path('article/<int:pk>/test/js/', TestJsView.as_view(), name='test_js'),

    path('like/<str:content_type>/<int:object_id>/', LikeToggleView.as_view(), name='like_toggle'),

]