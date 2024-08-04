from django.urls import path , include
from .views import LoginApiView , CreateUsersApiView , DeleteCustomUserApiView , TeachersListApiView , StudentsListApiView , UpdateAccountApiView


urlpatterns = [
    path("login/", LoginApiView.as_view(), name="login"),
    path('create-account/', CreateUsersApiView.as_view(), name='signup'),
    path('teachers/', TeachersListApiView.as_view(), name='teahcers'),
    path('students/', StudentsListApiView.as_view(), name='students'),
    path('delete-account/<str:id>/', DeleteCustomUserApiView.as_view(), name='delete-user'),
    path('update-account/<str:id>/', UpdateAccountApiView.as_view(), name="update"),
]
