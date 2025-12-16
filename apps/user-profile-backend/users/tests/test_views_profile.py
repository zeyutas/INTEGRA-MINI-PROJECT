from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class UserProfileViewSmokeTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="viewuser",
            email="viewuser@example.com",
            password="password123",
            first_name="Ada",
            last_name="Lovelace",
            advisor_id="ADV8000",
            firm_name="FinCorp",
            role="Advisor",
            bio="Bio text",
            avatar_url="https://example.com/avatar.png",
        )
        cls.url = reverse("user_profile")

    def authenticate(self):
        self.client.force_authenticate(user=self.user)

    def test_get_requires_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_returns_own_profile(self):
        self.authenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["advisor_id"], self.user.advisor_id)

    def test_patch_updates_editable_fields(self):
        self.authenticate()
        payload = {"first_name": "Grace", "bio": "Updated"}
        response = self.client.patch(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Grace")
        self.assertEqual(self.user.bio, "Updated")
