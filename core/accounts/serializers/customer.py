from rest_framework import serializers
from accounts.models import User, Customer


class CustomerRegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    age = serializers.IntegerField(write_only=True)
    address = serializers.CharField(write_only=True)
    location = serializers.CharField(write_only=True)

    class Meta:
        model = User  # or adjust to the correct model
        fields = ['email', 'password', 'first_name', 'last_name', 'age', 'address', 'location']

    def create(self, validated_data):
        customer_fields = {
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'age': validated_data.pop('age'),
            'address': validated_data.pop('address'),
            'location': validated_data.pop('location'),
        }
        user = User.objects.create_user(**validated_data)
        Customer.objects.create(user=user, **customer_fields)
        return user
