from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserProfileSerializer
from django.db import transaction  # Recommended for ensuring atomicity during update

# Note: If real caching is implemented, you would import the client here, e.g.:
# from django.core.cache import cache 

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Handles GET /api/user/profile/ (Retrieve) 
    and PATCH /api/user/profile/ (Partial Update).
    
    Business Logic: Allows an authenticated Advisor to view/modify their own profile details.
    
    Scaling Note: This class is pre-wired to implement a Cache-Aside strategy 
    for scalability (e.g., using Redis) to handle read-heavy traffic.
    """
    serializer_class = UserProfileSerializer
    # Security: Only users with a valid JWT token can access this view.
    permission_classes = [permissions.IsAuthenticated]

    # --- GET (Retrieve) Logic: Demonstrates Cache-Aside Read ---
    def get_object(self):
        """
        Retrieves the user profile object, implementing the Cache-Aside read flow.
        """
        user = self.request.user
        # user_id_key = f'user_profile:{user.id}' # Future cache key
        
        # 1) Try read user profile from cache (e.g., Redis)
        # cached_data = cache.get(user_id_key) 
        # if cached_data:
        #     return cached_data # Cache Hit: Return cached data immediately
        
        # 2) Cache Miss: Hit the primary database
        profile_object = user # DRF efficiently retrieves the user object here.
        
        # 3) Populate cache: Set the data back into the cache with a TTL (e.g., 5m)
        # cache.set(user_id_key, profile_object, timeout=60*5)
        
        return profile_object

    # --- PATCH (Update) Logic: Demonstrates Cache Invalidation ---
    def update(self, request, *args, **kwargs):
        """
        Updates the user profile and ensures cache consistency (Cache Invalidation).
        """
        
        # Best Practice: Use transaction.atomic to ensure DB write succeeds entirely or fails entirely.
        # with transaction.atomic():
        
        # 1. Execute the standard update process (Write to DB)
        response = super().update(request, *args, **kwargs)

        # 2. Cache Invalidation: Only if the database write was successful (HTTP 200 OK)
        if response.status_code == status.HTTP_200_OK:
            # user_id_key = f'user_profile:{self.request.user.id}'
            # cache.delete(user_id_key)  # Evict the stale data from the cache.
            pass # Current Mini Project scope: placeholder for cache invalidation.
        
        return response