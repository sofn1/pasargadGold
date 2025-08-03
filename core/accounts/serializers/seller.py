from rest_framework import serializers
from accounts.models import User


class SellerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'age', 'phone_number', 'email', 'about_us',
            'profile_image', 'address', 'location', 'business_name', 'business_code', 'password'
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
            about_us=validated_data.get('about_us'),
            profile_image=validated_data.get('profile_image'),
            address=validated_data.get('address'),
            location=validated_data.get('location'),
            business_name=validated_data['business_name'],
            business_code=validated_data['business_code'],
            password=validated_data['password'],
            is_seller=True
        )
        return user


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'is_seller']

