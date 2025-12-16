from datetime import timedelta
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
import factory
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating B2B Advisor User objects.
    Ensures test data is consistent with the custom User model fields.
    """
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"advisor{n}") # Ensures unique usernames
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    first_name = "Ada"
    last_name = "Lovelace"
    advisor_id = factory.Sequence(lambda n: f"ADV{n:04d}") # Unique B2B ID
    firm_name = "FinCorp"
    role = "Senior Advisor"
    bio = "I help with SMSFs."
    avatar_url = "https://example.com/avatar.png"
    # Sets the password securely during user creation
    password = factory.PostGenerationMethodCall("set_password", "password123")


class UserProfileAPITests(APITestCase):
    """
    Tests the CRUD (Retrieve/Update) operations and security constraints 
    on the B2B Advisor User Profile endpoint.
    """
    url = reverse("user_profile")
    login_url = reverse("token_obtain_pair")
    
    @classmethod
    def setUpTestData(cls):
        """Sets up initial test data once per class run for performance."""
        # Using factory to create the user directly in the database
        cls.user = UserFactory() 

    def authenticate(self):
        """Helper to bypass the login step using DRF's force_authenticate (faster Unit Testing)."""
        self.client.force_authenticate(user=self.user)

    def patch_profile(self, payload):
        """Helper to consistently send a PATCH request with JSON payload."""
        return self.client.patch(self.url, payload, format="json")

    # =========================================================================
    # 1. SECURITY & PERMISSIONS TESTS (Ensure B2B Firewall is up)
    # =========================================================================

    def test_profile_requires_authentication(self):
        """Must return 401 if no credentials are provided (Access Control)."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_requires_authentication(self):
        """Must return 401 if patching without authentication."""
        response = self.client.patch(self.url, {"bio": "New bio"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_invalid_token_denied(self):
        """Ensures the API rejects malformed or fabricated tokens."""
        token = "invalid.token.value"
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_expired_token_denied(self):
        """Ensures the API rejects tokens past their expiry time (Security Best Practice)."""
        token = AccessToken.for_user(self.user)
        # Set expiration to 60 seconds in the past
        token.set_exp(from_time=timezone.now(), lifetime=timedelta(seconds=-60)) 
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # =========================================================================
    # 2. RETRIEVE (GET) TESTS
    # =========================================================================

    def test_get_profile_returns_current_user(self):
        """Verifies that the API returns all necessary B2B fields on successful authentication."""
        self.authenticate()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assert that core custom fields and inherited fields are present and correct
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["advisor_id"], self.user.advisor_id)
        self.assertEqual(response.data["firm_name"], self.user.firm_name)
        self.assertIn("date_joined", response.data) # Check for necessary default fields

    # =========================================================================
    # 3. UPDATE (PATCH) TESTS - BUSINESS LOGIC & CONSTRAINTS
    # =========================================================================

    def test_patch_read_only_fields_are_ignored(self):
        """CRITICAL CHECK: Ensures sensitive fields (e.g., email, advisor_id) cannot be changed."""
        self.authenticate()
        read_only_attempts = {
            "email": "new@example.com",
            "advisor_id": "ADV777",
            "firm_name": "OtherFirm", # Firm Name is Read-Only
            "username": "different",
        }

        response = self.patch_profile(read_only_attempts)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        
        # Verify that ALL attempted changes were ignored in the database
        for field, attempted in read_only_attempts.items():
            with self.subTest(field=field):
                # We assert that the database value is NOT the attempted value
                self.assertNotEqual(getattr(self.user, field), attempted)

    def test_patch_updates_only_editable_fields(self):
        """Verifies successful update of permitted fields (names, bio, avatar)."""
        self.authenticate()
        payload = {
            "first_name": "Grace",
            "last_name": "Hopper",
            "bio": "Updated bio text",
            "avatar_url": "https://example.com/new-avatar.png",
        }
        
        # Include read-only attempts to ensure they are ignored even in a valid request
        payload["advisor_id"] = "HACKED_ID" 

        response = self.client.patch(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()

        # Assert successful update of editable fields
        self.assertEqual(self.user.first_name, payload["first_name"])
        self.assertEqual(self.user.last_name, payload["last_name"])
        self.assertEqual(self.user.bio, payload["bio"])
        
        # Assert read-only field was ignored
        self.assertNotEqual(self.user.advisor_id, "HACKED_ID")

    def test_patch_partial_does_not_clear_unsent_fields(self):
        """PATCH should update only sent fields and keep others unchanged."""
        self.authenticate()
        original_last_name = self.user.last_name

        response = self.patch_profile({"first_name": "Grace"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Grace")
        self.assertEqual(self.user.last_name, original_last_name)

    def test_patch_rejects_invalid_avatar_url(self):
        """Ensures the URLField validation prevents injection or malformed data."""
        self.authenticate()
        bad_url = "not-a-url"

        response = self.client.patch(self.url, {"avatar_url": bad_url}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertEqual(self.user.avatar_url, "https://example.com/avatar.png") # Should remain original

    def test_patch_rejects_avatar_url_variants(self):
        """Common malformed or unsafe avatar URLs should all be rejected."""
        self.authenticate()
        bad_values = ["", "www.example.com/avatar.png", "javascript:alert(1)", "ftp://example.com"]

        for value in bad_values:
            with self.subTest(value=value):
                response = self.patch_profile({"avatar_url": value})
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.user.refresh_from_db()
                self.assertEqual(self.user.avatar_url, "https://example.com/avatar.png")
                self.authenticate()  # Reset auth after each loop

    def test_patch_allows_empty_names(self):
        """Names are optional; empty strings should be accepted."""
        self.authenticate()
        payload = {"first_name": "", "last_name": ""}

        response = self.patch_profile(payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")

    def test_patch_allows_large_bio_within_limit(self):
        """A reasonably large bio under max_length should succeed."""
        self.authenticate()
        long_bio = "A" * 900  # under max_length=1024

        response = self.patch_profile({"bio": long_bio})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, long_bio)

    def test_patch_rejects_overlong_bio(self):
        """Tests the max_length constraint added to the bio field."""
        self.authenticate()
        too_long_bio = "B" * 2000  # exceeds max_length=1024

        response = self.patch_profile({"bio": too_long_bio})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.bio, too_long_bio)

    def test_patch_rejects_overlong_first_name(self):
        """First name max_length=50 enforced."""
        self.authenticate()
        too_long = "F" * 60  # max_length enforced at 50

        response = self.patch_profile({"first_name": too_long})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.first_name, too_long)

    def test_patch_rejects_overlong_last_name(self):
        """Last name max_length=50 enforced."""
        self.authenticate()
        too_long = "L" * 60  # max_length enforced at 50

        response = self.patch_profile({"last_name": too_long})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.last_name, too_long)

    def test_patch_rejects_overlong_firm_name(self):
        """Tests the max_length constraint on a Read-Only field (Serializer validation check)."""
        self.authenticate()
        too_long = "Firm" * 40 # Assuming max_length=150

        response = self.patch_profile({"firm_name": too_long})

        # Even though Read-Only fields are ignored, validation should fail first if constraints are broken
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.firm_name, too_long)
