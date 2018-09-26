"""project_team_builder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"logout/$", views.LogoutView.as_view(), name="logout"),
    url(r"login/$", views.LoginView.as_view(), name="sign_in"),
    url(r"signup/$", views.SignUpView.as_view(), name="sign_up"),
    url(r"profile/(?P<pk>\d+)/$", views.ProfileDetailView.as_view(),
        name="profile"),
    url(r'edit/(?P<pk>\d+)/$', views.ProfileEditView.as_view(),
        name='profile_edit'),
]
