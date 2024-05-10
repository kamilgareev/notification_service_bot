from datetime import datetime, timezone
from rest_framework import serializers

from .models import Notification


class NotificationCreateViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

    def validate_time(self, value):
        if value <= datetime.now(tz=timezone.utc):
            raise serializers.ValidationError(f'Invalid notification time.')
        return value


class NotificationRetrieveViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
