from django.conf.urls.static import static, settings
from django.urls import path
from . import views


urlpatterns = [

    path('', views.search, name='search'),
    path('result-<str:text_search>', views.search_result, name='search_result'),
    path('result/people-<str:text_search>', views.search_result_people, name='search_result_people'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


