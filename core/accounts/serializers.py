from rest_framework import serializers
from .models import User, Customer, Seller, Writer


# ====== Base User Serializer ======
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'role']


# ====== Register Customer ======
class CustomerRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ['user', 'first_name', 'last_name', 'age', 'address', 'location']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(
            phone_number=user_data['phone_number'],
            password='default_password',  # override later
            role='customer'
        )
        user.set_password(self.context['request'].data.get('password'))
        user.save()
        customer = Customer.objects.create(user=user, **validated_data)
        return customer


# ====== Register Seller ======
class SellerRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Seller
        fields = ['user', 'first_name', 'last_name', 'age', 'email', 'about_us', 'profile_image',
                  'address', 'location', 'business_name', 'business_code']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(
            phone_number=user_data['phone_number'],
            password='default_password',
            role='seller'
        )
        user.set_password(self.context['request'].data.get('password'))
        user.save()
        seller = Seller.objects.create(user=user, **validated_data)
        return seller


# ====== Register Writer ======
class WriterRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Writer
        fields = ['user', 'first_name', 'last_name', 'age', 'email', 'about_me', 'profile_image']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(
            phone_number=user_data['phone_number'],
            password='default_password',
            role='writer'
        )
        user.set_password(self.context['request'].data.get('password'))
        user.save()
        writer = Writer.objects.create(user=user, **validated_data)
        return writer
