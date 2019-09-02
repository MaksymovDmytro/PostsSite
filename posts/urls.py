from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import PostList, PostDetail, PostCreate, PostUpdate, delete_post_view, add_comment_view, like_post_view


app_name = 'posts'
redirect_url = '/accounts/login'

urlpatterns = [
    path('', login_required(PostList.as_view(), login_url=redirect_url), name='list_view'),
    path('create/', login_required(PostCreate.as_view(), login_url=redirect_url), name='create_view'),
    path('<int:pk>/update/', login_required(PostUpdate.as_view(), login_url=redirect_url), name='update_view'),
    path('<int:pk>/delete/', login_required(delete_post_view, login_url=redirect_url), name='delete_view'),
    path('<int:pk>/', login_required(PostDetail.as_view(), login_url=redirect_url), name='details_view'),
    path('<int:pk>/like/', login_required(like_post_view, login_url=redirect_url), name='likes_view'),
    path('<int:pk>/comment/', login_required(add_comment_view, login_url=redirect_url), name='comment_view'),
]
