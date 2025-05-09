from rest_framework import serializers
from .models import SeekerProfile, ProviderProfile
from users.serializers import UserDetailSerializer # To nest user details if needed

class SeekerProfileSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True) # Or serializers.PrimaryKeyRelatedField for write

    class Meta:
        model = SeekerProfile
        fields = '__all__'
        read_only_fields = ('user',) # User is set automatically

class ProviderProfileSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = ProviderProfile
        fields = '__all__'
        read_only_fields = ('user',)