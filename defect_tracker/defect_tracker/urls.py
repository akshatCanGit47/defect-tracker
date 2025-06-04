# defect_tracker/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.project_list, name='home'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_pk>/defects/create/', views.create_defect, name='create_defect'),
    path('projects/<int:project_pk>/add-member/', views.add_member, name='add_member'),
    path('defects/<int:pk>/update/', views.update_defect, name='update_defect'),
]