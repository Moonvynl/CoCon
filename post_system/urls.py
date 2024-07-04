from django.urls import path
from django.urls import reverse_lazy
from .views import *

urlpatterns = [
    path('create-post/', CreatePostView.as_view(), name='create-post'),
]

app_name = 'post_system'