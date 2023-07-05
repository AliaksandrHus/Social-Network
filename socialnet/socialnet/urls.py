from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('account.urls')),
    path('news/', include('news.urls')),
    path('search/', include('search.urls')),
    path('groups/', include('groups.urls')),
    path('messages/', include('usermessages.urls')),

    # path('admin/', include('useradmin.urls')),
]
