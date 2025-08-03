from rest_framework import serializers
from django.utils.timezone import now
from datetime import timedelta


class DateRangeFilterSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)

    def validate(self, data):
        today = now().date()
        data['start_date'] = data.get('start_date') or (today - timedelta(days=6))
        data['end_date'] = data.get('end_date') or today
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("start_date must be before end_date")
        return data
