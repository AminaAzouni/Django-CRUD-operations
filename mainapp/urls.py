from django.urls import path
from mainapp import views
urlpatterns= [
      path('', views.home, name='home'),
      path('login/', views.user_login, name='login'),
      path('signup/', views.user_signup, name='signup'),
      path('logout/', views.user_logout, name='logout'),
      path('create/', views.create_student, name='create'),
      path('detail/<int:pk>', views.view_student, name='detail'),
      path('update/<int:pk>', views.update_student, name='update'),
      path('delete/<int:pk>', views.delete_student, name='delete'),

       
]