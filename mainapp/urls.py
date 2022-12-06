from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static

app_name='mainapp_app'
urlpatterns = [
    path('',views.hello,name='inicio'),
    path('file',views.FileUploadView.as_view(),name='file'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)