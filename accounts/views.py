from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import SignUpSerializer

User = get_user_model()


class SignUpView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    lookup_field = 'id'
