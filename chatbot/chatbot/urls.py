from django.contrib import admin
from django.urls import path, re_path
from adminsite.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_page, name='login_page'),
    path('login_user/', login_user, name='login_user'), 
    path('admin/dashboard/', admin_account, name='admin_account'),
    path('curator/dashboard/', curator_account, name='curator_account'),
    re_path(r'young_employees/$', young_employee_list),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)