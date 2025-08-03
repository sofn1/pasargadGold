from rest_framework import serializers
from accounts.models import User


class WriterRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'age', 'phone_number', 'email',
            'about_me', 'profile_image', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            age=validated_data['age'],
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
            about_me=validated_data.get('about_me'),
            profile_image=validated_data.get('profile_image'),
            password=validated_data['password'],
            is_writer=True
        )
        return user