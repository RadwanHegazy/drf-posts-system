from . import views
from django.urls import path


urlpatterns = [

    # authentication
    path('register/',views.RegisterView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),

    # view or create posts
    path('',views.ViewPosts,name='posts'),
    
    # edit or delete posts
    path('<int:postid>/',views.UserPost,name='user_post'),


]