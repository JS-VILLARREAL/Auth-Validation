from django.urls import path, re_path

from . import views

app_name = 'users'

urlpatterns = [
    re_path('register-by-access-token/' + r'social/(?P<backend>[^/]+)/$', views.register_by_access_token),
    path('authentication-test/', views.authentication_test),
    
    # path('validate-google-token/', views.validate_google_token, name='validate_google_token'),
    # path('auth/', views.validate_google_token, name='google-auth'),
]