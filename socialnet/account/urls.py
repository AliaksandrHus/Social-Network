from django.conf.urls.static import static, settings
from django.urls import path
from . import views


urlpatterns = [

    path('', views.index, name='index'),

    path('profile_page', views.profile_page, name='profile_page'),
    path('user-<int:pk>', views.another_user_page, name='another_user_page'),

    path('settings_page', views.settings_page, name='settings_page'),

    path('login_page', views.login_page, name='login_page'),
    path('logout_page', views.logout_page, name='logout_page'),
    path('registration_page', views.registration_page, name='registration_page'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


