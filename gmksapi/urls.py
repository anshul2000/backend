from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = "api"
urlpatterns = [
    path('', views.home, name="home"),
    path('api/messages/', views.create_message, name="messages"),
    path('api/', views.data_list, name="api"),
    path('api/<str:pk>/', views.data, name="api1"),
    path('api1/event/Download',views.event_download,name="event"),
    re_path(r'api1/(?P<pk>.+)/(?P<location>.+)/(?P<lang>.+)$', views.download, name="api2"),
    path('number/',csrf_exempt(views.number) ,name='number'),
    path('number2/',csrf_exempt(views.number2) ,name='number2'),
    path('sms/',csrf_exempt(views.sms) ,name='sms'),
    path('text/',csrf_exempt(views.text) ,name='text'),
    path('awareness/',csrf_exempt(views.awareness) ,name='awareness'),
    path('awareness/<int:id>',csrf_exempt(views.awareness_download), name='awareness_download'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
