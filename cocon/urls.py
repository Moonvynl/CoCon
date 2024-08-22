from django.urls import path
from django.urls import reverse_lazy
from .views import *

urlpatterns = [
    path('', NewsFeedView.as_view(), name='newsfeed'),
    path('leftmenu/', LeftMenuView.as_view(), name='leftmenu'),
    path('search/', search_view, name='search'),
    path('search/results/<str:choose_output>/', search_results, name='search_results'),
    path('interestings/', InterestingsView.as_view(), name='interestings'),
]

app_name = 'cocon'