from django.urls import path
from blogapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('blog/', views.blog, name='blog'),
    path('about', views.about, name='about'),
    path('post/<slug:slug>', views.post, name='post'),
    path('category/<slug:slug>', views.category, name='category'),
    path('addpost/', views.add_post, name='addpost'),
    path('search/',views.search_post, name='search'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('deletepost/<int:id>',views.delete_post,name='deletepost'),
    path('admindeletepost/<int:id>',views.admin_delete_home,name='admindeletepost'),
    path('admindeleteblog/<int:id>',views.admin_delete_blog,name='admindeleteblog'),
    path('updatepost/<int:id>',views.update_post,name='updatepost'),
    path('adminupdatepost/<slug:slug>',views.admin_update_post,name='adminupdatepost'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('signup/', views.user_signup, name='signup'),
    path('account-verify/<slug:token>', views.user_account_verify, name='account-verify'),

    path('password-change/', views.user_password_change, name='change-password'),
    path('password-reset/<slug:token>', views.user_password_reset, name='reset-password'),
    path('user-email-send/', views.user_email_send, name='send-email'),
        
    ]