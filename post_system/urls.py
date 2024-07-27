from django.urls import path
from django.urls import reverse_lazy
from .views import *

urlpatterns = [
    path('create-post/', CreatePostView.as_view(), name='create-post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('get_model_data/<int:pk>/', get_model_data, name='post-data'),
    path('like-post/', like_post, name='like-post'),
    path('comment-post', comment_post, name='comment-post'),

]

app_name = 'post_system'