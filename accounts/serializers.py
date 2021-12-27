from django.contrib.auth.models import User
from rest_framework import serializers
from stack_app.models import Question


class UserSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'confirmPassword']
    

    # def create(self, validated_data):
    #     user = User.objects.create(username=validated_data['username'])
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user