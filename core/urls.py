from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.registration_view, name='register'),
    path('profile/<int:pk>/', views.profile_view, name='profile'),
    path('profile/<int:pk>/update/', views.update_profile_view, name='update-profile'),
    path('dep/', views.dep_view, name='dep'),
    path('major/', views.major_view, name='major'),
    path('classroom/', views.class_view, name='classroom'),
    path('course/', views.course_view, name='course'),
    path('teacher/', views.teacher_view, name='teacher'),

    path('edit-score-detail/<int:pk>/', views.edit_score_detail_view, name='edit-score-detail'),
]
