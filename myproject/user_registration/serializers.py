from rest_framework import serializers
from .models import UserModel
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ('email', 'password')

    def validate_email(self, value):
        try:
            UserModel.objects.get(email=value)
        except UserModel.DoesNotExist:
            return value
        else:
            raise serializers.ValidationError("Email is already taken")

    def validate_password(self, value):
        passwd = len(value)
        if passwd and passwd < 8:
            raise ValidationError("Password must be greater than 8 characters")
        return str(value)

    def create(self, validated_data):
        return UserModel.objects.create_user(**validated_data)