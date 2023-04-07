from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# Создаем роутер и регистрируем необходимые ViewSets
router = DefaultRouter()
# Регистрируем GroupViewSet с роутером
router.register('groups', views.GroupViewSet)
# Регистрируем PostViewSet с роутером
router.register('posts', views.PostViewSet)
# Регистрируем CommentViewSet с роутером
# Параметр post_id используется для получения комментариев к конкретному посту
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    views.CommentViewSet,
    basename='Comment'
)


urlpatterns = [
    path('v1/follow/', views.FollowView.as_view()),
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
