from django.test import TestCase
from django.contrib.auth import get_user_model

from .serializers import UserProfileSerializer


User = get_user_model()


class UserProfileSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="serializer_user",
            email="serializer_user@example.com",
            password="password123",
            first_name="Ada",
            last_name="Lovelace",
            advisor_id="ADV9000",
            firm_name="FinCorp",
            role="Senior Advisor",
            bio="Bio text",
            avatar_url="https://example.com/avatar.png",
        )

    def test_valid_partial_update_applies_editable_fields(self):
        data = {
            "first_name": "Grace",
            "bio": "Updated bio",
            "avatar_url": "https://example.com/new.png",
        }
        serializer = UserProfileSerializer(instance=self.user, data=data, partial=True)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()

        self.assertEqual(instance.first_name, data["first_name"])
        self.assertEqual(instance.bio, data["bio"])
        self.assertEqual(instance.avatar_url, data["avatar_url"])

    def test_read_only_fields_not_applied_on_update(self):
        data = {
            "advisor_id": "HACKED",
            "firm_name": "OtherFirm",
        }
        serializer = UserProfileSerializer(instance=self.user, data=data, partial=True)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        validated = serializer.validated_data
        self.assertNotIn("advisor_id", validated)
        self.assertNotIn("firm_name", validated)

    def test_invalid_avatar_scheme_rejected(self):
        data = {"avatar_url": "ftp://example.com/avatar.png"}
        serializer = UserProfileSerializer(instance=self.user, data=data, partial=True)

        self.assertFalse(serializer.is_valid())
        self.assertIn("avatar_url", serializer.errors)

    def test_overlong_firm_name_rejected(self):
        data = {"firm_name": "X" * 200}
        serializer = UserProfileSerializer(instance=self.user, data=data, partial=True)

        self.assertFalse(serializer.is_valid())
        self.assertIn("firm_name", serializer.errors)

    def test_overlong_first_name_rejected(self):
        data = {"first_name": "F" * 60}
        serializer = UserProfileSerializer(instance=self.user, data=data, partial=True)

        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)
