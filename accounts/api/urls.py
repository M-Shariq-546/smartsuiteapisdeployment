from django.urls import path , include
from .views import *

urlpatterns = [
    path("login/", LoginApiView.as_view(), name="login"),
    path('create-account/', CreateUsersApiView.as_view(), name='signup'),
    path('teachers/', TeachersListApiView.as_view(), name='teahcers'),
    path('students/', StudentsListApiView.as_view(), name='students'),
    path('super_admin_graph_data/', StudentCountView.as_view(), name='studentCounts'),
    path('teachers_graph_data/', TeacherGetDataApiView.as_view(), name='teachers_get_data'),

    path('student_graph_data/', StudentGetDataApiView.as_view(), name='student_graph_data'),

    path('delete-account/<str:id>/', DeleteCustomUserApiView.as_view(), name='delete-user'),
    path('update-account/<str:id>/', UpdateAccountApiView.as_view(), name="update"),
]
