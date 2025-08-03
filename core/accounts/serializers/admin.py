from rest_framework import serializers
from accounts.models import AdminPermission
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminPermissionSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user')

    class Meta:
        model = AdminPermission
        fields = ['id', 'user_id', 'is_superadmin']
