
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic import TemplateView
from app_1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',views.home, name='home'),

    path('login/',LoginView.as_view(template_name='auth/login.html'),name='login'),
    path('logout/', LogoutView.as_view(template_name='auth/logout.html'), name='logout'),

    path('document_add/',views.document_add,name='document_add'),
    path('document_all/',views.document_all,name='document_all'),
    path('document_edit/<int:document_id>/',views.document_edit,name='document_edit'),
    path('document_delete/<int:document_id>/',views.document_delete,name='document_delete'),

    path('user_add/',views.user_add,name='user_add'),
    path('user_all/',views.user_all,name='user_all'),
    path('user_edit/<int:user_id>/',views.user_edit,name='user_edit'),
    path('user_delete/<int:user_id>/',views.user_delete,name='user_delete'),

    path('document_list_shared/',views.document_list_shared,name="document_list_shared"),
    path('document_list_shared/<int:filter>',views.document_list_shared,name="document_list_shared"),
    path('document_list_shared/<str:sort>',views.document_list_shared,name="document_list_shared"),

    path('document_count/',views.document_count,name='document_count'),
    path('student_count/',views.student_count,name='student_count'),
    path('document_details/<int:document_id>',views.document_details, name="document_details"),
    path('professor_details/<int:user_id>',views.professor_details, name="professor_details"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)