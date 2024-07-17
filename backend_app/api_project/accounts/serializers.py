from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.registration.views import get_adapter
from rest_framework import serializers
from .models import Users

class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.username = self.cleaned_data.get('username')
        user.email = self.cleaned_data.get('email')
        user.set_password(self.cleaned_data.get('password1'))
        user.save()
        adapter.save_user(request, user, self)
        return user

