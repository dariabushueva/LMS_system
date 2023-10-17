from rest_framework import serializers

from lms.serializers import PaymentSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payment_history = PaymentSerializer(source='payment_set', read_only=True, many=True)

    class Meta:
        model = User
        fields = ('last_login', 'id', 'email', 'password', 'phone', 'city', 'avatar', 'payment_history', 'is_active')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
