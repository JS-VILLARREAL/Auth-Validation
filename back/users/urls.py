from django.urls import path, re_path

from . import views

app_name = 'users'

urlpatterns = [
    re_path('register-by-access-token/' + r'social/(?P<backend>[^/]+)/$', views.register_by_access_token),
    path('authentication-test/', views.authentication_test),
    
    re_path('register-by-access-token-facebook/' + r'social/(?P<backend>[^/]+)/$', views.register_by_access_token_facebook),
    # re_path('validate-facebook-token/', views.validate_facebook_token, name='validate_facebook_token'),
]