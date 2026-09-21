from django.urls import path
from . import views
from .views import PostListView, UserPostDetailView, PostCreateView, PostUpdateView, PostDeleteView, PostDetailView

urlpatterns = [
    path('', PostListView.as_view(), name="blog-home"),
    path('user/<str:username>/', UserPostDetailView.as_view(), name="user-posts"),
    path('post/<int:pk>', PostDetailView.as_view(), name="posts-detail"),
    path('post/new/', PostCreateView.as_view(), name="post-create"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name="blog-about"),
    path('latest-posts/', views.latest_posts, name='latest-posts'),
    path('oldest-posts/', views.oldest_posts, name='oldest-posts'),
    path('contact/', views.contact, name='contact'),
    path('post/<int:pk>/like/', views.post_like, name='post-like'),
    path('post/<int:pk>/dislike/', views.post_disliked, name='post-dislike'),
    path('comment/<int:comment_id>/delete', views.delete_comment, name='comment-delete'),
    path('intro/', views.intro, name='intro')
]
 