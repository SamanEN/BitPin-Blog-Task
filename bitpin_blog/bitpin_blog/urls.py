from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('blogs/', include('blog_posts.urls')),
    path('rate/', include('rate.urls'))
]
