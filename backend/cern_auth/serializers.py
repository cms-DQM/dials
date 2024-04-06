from rest_framework import serializers


class ExchangedTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    expires_in = serializers.IntegerField()
    refresh_expires_in = serializers.IntegerField()
    refresh_token = serializers.CharField()
    token_type = serializers.CharField()
    id_token = serializers.CharField()
    session_state = serializers.CharField()
    scope = serializers.CharField()


class DeviceSerializer(serializers.Serializer):
    device_code = serializers.CharField()
    verification_uri_complete = serializers.CharField()
    expires_in = serializers.IntegerField()


class DeviceTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    expires_in = serializers.IntegerField()
    refresh_expires_in = serializers.IntegerField()
    refresh_token = serializers.CharField()
    token_type = serializers.CharField()
    session_state = serializers.CharField()
    scope = serializers.CharField()


class PendingAuthorizationErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()
    code = serializers.CharField()
