from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import CompleteSignView, QuitView, BaseRegisterView, GetOneTimeCode, PostCodeView

urlpatterns = [
    path('complete/', CompleteSignView.as_view()),
    path('quit/', QuitView.as_view()),
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(), name='signup'),
    path('code_confirm/', GetOneTimeCode.as_view(), name='code_confirm'),
    path('post_code/', PostCodeView.as_view(), name='post_code'),
]
