from django.contrib import admin
from django.urls import path, re_path
from adminsite.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_page, name='login_page'),
    path('login_user/', login_user, name='login_user'), 
    path('admin_account/', admin_account, name='admin_account'),
    path('curator_account/', curator_account, name='curator_account'),
    re_path('young_employees/', young_employee_list, name='young_employee_list'),
    path('chats/', chats, name='chats'),
    path('chat/<int:employee_id>/', chat_with_employee, name='chat_with_employee'),
    path('report/', report_page, name='report_page'),
    path('download/', download_report, name='download_report'),
    path('statistic/', statistic, name='statistic'),
    path('employee/<int:employee_id>/', employee, name='employee'),
    path('filter_employees/', filter_employees, name='filter_employees'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)