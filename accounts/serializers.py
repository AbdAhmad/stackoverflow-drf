from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'confirmPassword']

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        confirmPassword = attrs['confirmPassword']

        try:
            username_zero_idx = int(username[0])
            if isinstance(username_zero_idx, int):
                raise serializers.ValidationError('Username cannot start with a number')
        except ValueError:
            pass

        if len(username) < 4:
            raise serializers.ValidationError('Username is too short')

        if username.isdigit():
            raise serializers.ValidationError('Username cannot be entirely numeric')

        if len(password) < 8:
            raise serializers.ValidationError('Password is too short')

        if password.isdigit():
            raise serializers.ValidationError('Password cannot be entirely numeric')

        if password != confirmPassword:
            raise serializers.ValidationError('Two passwords do no match')

        return super().validate(attrs)



