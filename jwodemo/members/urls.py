from django.urls import path
from . import views
from .views import ShowProfilePageView, EditProfilePageView
from .views import edit_profile, UserEditView, PasswordsChangeView

urlpatterns=[
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout"),
    path('register_user', views.register_user, name="register_user"),
    path('account', views.account, name="account"),
    path('edit_profile/', edit_profile, name='edit_profile'),

    path('blog_edit_profile/', UserEditView.as_view(), name='blog_edit_profile'),
    path('<int:pk>/profile/', ShowProfilePageView.as_view(), name='show_profile_page'),
    path('<int:pk>/edit_profile_page/', EditProfilePageView.as_view(), name='edit_profile_page'),
    path('password/', PasswordsChangeView.as_view(template_name='registration/change-password.html'), name='password_change'),

    path('password_success', views.password_success, name='password_success'),


]