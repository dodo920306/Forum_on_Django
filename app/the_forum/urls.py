from django.urls import path, include
from . import views


urlpatterns = [
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
    path('', views.index, name='index'),
    path(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),
    path('accounts/profile/', views.profile, name='profile'),
    path('board/', views.board, name='board'),
    path('post/', views.post, name='post'),
    path('create_post/', views.create_post, name='create_post'),
    path('delete_post/', views.delete_post, name='delete_post')
]
