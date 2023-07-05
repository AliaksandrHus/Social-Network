from django.conf.urls.static import static, settings
from django.urls import path
from . import views


urlpatterns = [

    path('', views.all_messages, name='all_messages'),
    path('dialog-<int:dialog_id>', views.dialog, name='dialog'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

