from rest_framework.viewsets import ModelViewSet
from ..models import History
from .serializers import HistorySerializers

class HistoryListApiView(ModelViewSet):
    serializer_class = HistorySerializers
    queryset = History.objects.all().order_by('-timestamp' and '-id')

    def get_queryset(self):
        user = self.request.user
        return History.objects.filter(user=user).order_by('-timestamp' and '-id' )
