from django.urls import path , include
from .views import *

urlpatterns = [
    path("login/", LoginApiView.as_view(), name="login"),
    path('create-account/', CreateUsersApiView.as_view(), name='signup'),
    path('teachers/', TeachersListApiView.as_view(), name='teahcers'),
    path('students/', StudentsListApiView.as_view(), name='students'),
    path('graph_data/', StudentCountView.as_view(), name='studentCounts'),
    path('delete-account/<str:id>/', DeleteCustomUserApiView.as_view(), name='delete-user'),
    path('update-account/<str:id>/', UpdateAccountApiView.as_view(), name="update"),
]
