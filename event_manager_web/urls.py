from django.contrib import admin
from django.urls import include, path

# Обработчик 404 для всего проекта (раздел 5.4.7 методички)
handler404 = 'homepage.views.page_not_found'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('events/', include('events_app.urls')),
    path('registrations/', include('registrations_app.urls')),
]