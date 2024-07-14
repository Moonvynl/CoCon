from django.urls import path
from django.urls import reverse_lazy
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('leftmenu/', LeftMenuView.as_view(), name='leftmenu'),
    path('search/', search_view, name='search'),
    path('search/results/', search_results, name='search_results'),
    
]

app_name = 'cocon'