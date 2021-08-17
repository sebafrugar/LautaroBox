from django.urls import path
from box import views



urlpatterns = [
    path('', views.home),
    path('', views.login),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('horarios/<str:dia>', views.horario_dia),
    path('planes', views.planes),
    path('tomar_clases', views.tomar_clases),
    path('store', views.store),
    path('compras', views.compras),
    path('delete/<int:id>', views.delete),

]