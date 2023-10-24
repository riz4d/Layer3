from django.urls import path

from . import views
urlpatterns = [
    path('',views.login),
    path('layer3',views.threelayercr),
    path('signup',views.signup),
    path("log3",views.home),
    path("home",views.logged),
    path("logout",views.logout)
]