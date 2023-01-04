from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static

app_name='mainapp_app'
urlpatterns = [
    path('',views.hello,name='inicio'),
    path('api/users/create',views.createUser().as_view(),name='registrar'),
    path('api/users',views.getUsers().as_view()),
    path('file',views.FileUploadView.as_view(),name='file'),
]+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
