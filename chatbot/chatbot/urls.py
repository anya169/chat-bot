from django.contrib import admin
from django.urls import path, re_path
from adminsite.views import *
from bot.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_page, name='login_page'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('', RedirectView.as_view(url='login/', permanent=False)),
    path('login_user/', login_user, name='login_user'), 
    path('curator_account/', curator_account, name='curator_account'),
    path('chats/', chats, name='chats'),
    path('chat/<int:employee_id>/', chat_with_employee, name='chat_with_employee'),
    path('report/', report_page, name='report_page'),
    path('download/', download_report, name='download_report'),
    path('statistic/', statistic, name='statistic'),
    path('employee/<int:employee_id>/', employee, name='employee'),
    path('filter_employees/', filter_employees, name='filter_employees'),
    path('answer_question/<int:question_id>/', answer_question, name='answer_question'),
    path('mailings/', mailings, name='mailings'),
    path('mailing/<int:mailing_id>/', mailing, name='mailing'),
    path('get_mailings/', get_mailings, name='get_mailings'),
    path('delete_mailing/', delete_mailing, name='delete_mailing'),
    path('send_mailing_to_employee/', send_mailing_to_employee, name='send_mailing_to_employee'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)