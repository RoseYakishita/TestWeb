from django.urls import path, include
from core.views import index, search_view, CreateUser, UpdateUser, DeleteUser

app_name = 'core'

urlpatterns = [
    path("", index, name='index'),
    path("search/", search_view, name='search'),
    path('create/', CreateUser.as_view(), name='CreateUser'),
    path('delete/<int:pk>/', DeleteUser.as_view(), name='DeleteUser'),
    path('update/<int:pk>/', UpdateUser.as_view(), name='UpdateUser'),

]