from rest_framework import viewsets
from app.models import Users
from app.serializers import UsersSerializer

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer