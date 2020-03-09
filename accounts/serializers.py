from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
