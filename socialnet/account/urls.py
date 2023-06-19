from django.conf.urls.static import static, settings
from django.urls import path
from . import views


urlpatterns = [

    path('', views.index, name='index'),

    path('profile_page', views.profile_page, name='profile_page'),
    path('profile_page/followers', views.profile_page_followers, name='profile_page/followers'),
    path('profile_page/following', views.profile_page_following, name='profile_page/following'),
    path('profile_page/photo', views.profile_page_photo, name='profile_page/photo'),
    path('profile_page/photo/show-<int:pk_photo>', views.profile_page_photo_show, name='profile_page/photo/show'),

    path('user-<int:pk>', views.another_user_page, name='another_user_page'),
    path('user-<int:pk>/followers', views.another_user_page_followers, name='another_user_page/followers'),
    path('user-<int:pk>/following', views.another_user_page_following, name='another_user_page/following'),
    path('user-<int:pk>/photo', views.another_user_page_photo, name='another_user_page/photo'),
    path('user-<int:pk>/photo/show-<int:pk_photo>', views.another_user_page_photo_show, name='another_user_page/photo/show'),

    path('settings_page', views.settings_page, name='settings_page'),

    path('login_page', views.login_page, name='login_page'),
    path('logout_page', views.logout_page, name='logout_page'),
    path('registration_page', views.registration_page, name='registration_page'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


