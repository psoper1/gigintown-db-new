from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        return token
    
    
class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'

class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class UserDetailsSerializer(serializers.ModelSerializer):
    saved_events = EventSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'account_type', 'saved_events',
                  'address', 'city', 'state', 'zipCode', 'businessName', 'website']


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    account_type = serializers.CharField(max_length=20, write_only=True)
    saved_events = serializers.PrimaryKeyRelatedField(many=True, queryset=Event.objects.all(), required=False)
    address = serializers.CharField(allow_null=True, required=False)
    city = serializers.CharField(allow_null=True, required=False)
    state = serializers.CharField(allow_null=True, required=False)
    zipCode = serializers.CharField(allow_null=True, required=False)
    businessName = serializers.CharField(allow_null=True, required=False)
    website = serializers.CharField(allow_null=True, required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name', 'account_type', 'saved_events',
                  'address', 'city', 'state', 'zipCode', 'businessName', 'website')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        account_type = validated_data.pop('account_type', 'General')
        saved_events_data = validated_data.pop('saved_events', [])
        instance = self.Meta.model(**validated_data, account_type=account_type)
        if password is not None:
            instance.set_password(password)
        instance.save()

        for event in saved_events_data:
            instance.saved_events.add(event)

        return instance