from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    avatar_url = serializers.URLField(required=False, allow_blank=False)
    bio = serializers.CharField(required=False, allow_blank=True, max_length=1024)
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=50)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=50)

    def validate_avatar_url(self, value):
        # Enforce http/https to avoid unsafe or malformed URLs.
        if value and not value.startswith(("http://", "https://")):
            raise serializers.ValidationError("Avatar URL must start with http:// or https://")
        return value

    def validate(self, attrs):
        # Enforce length on read-only fields when present to avoid noisy payloads.
        errors = {}
        firm_name = self.initial_data.get("firm_name")
        if firm_name is not None and len(firm_name) > 150:
            errors["firm_name"] = ["Ensure this field has no more than 150 characters."]
        if errors:
            raise serializers.ValidationError(errors)
        return super().validate(attrs)

    class Meta:
        model = User
        # Fields exposed to the frontend (must match the B2B Advisor JSON contract)
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'advisor_id', 'firm_name', 'role', 'bio', 'avatar_url',
            'date_joined' 
        ]
        
        # Fields that cannot be modified via a PATCH request from the portal user
        read_only_fields = [
            'id', 'username', 'email', 'advisor_id', 
            'firm_name', 'date_joined', 'role'
        ]
        # Note: Advisor ID and Firm Name must be managed by Admin, not the user.
