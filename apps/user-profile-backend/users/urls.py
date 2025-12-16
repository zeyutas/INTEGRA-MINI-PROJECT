from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# Import the custom views from the current application
from .views import UserProfileView 

urlpatterns = [
    # ========================================================================
    # 1. Authentication Endpoints (JWT Token Handling)
    # These routes handle user login and token refreshment.
    # Base URL Prefix: /api/
    # ========================================================================
    
    # POST /api/auth/login/
    # Takes credentials (username, password) and returns access and refresh tokens.
    path(
        'auth/login/', 
        TokenObtainPairView.as_view(), 
        name='token_obtain_pair'
    ),
    
    # POST /api/auth/refresh/
    # Takes a refresh token and returns a new access token.
    path(
        'auth/refresh/', 
        TokenRefreshView.as_view(), 
        name='token_refresh'
    ),
    
    # ========================================================================
    # 2. User Profile Endpoint (Authenticated Access Required)
    # This route allows for reading and updating the financial advisor's profile.
    # Base URL Prefix: /api/
    # ========================================================================

    # GET/PATCH /api/user/profile/
    path(
        'user/profile/', 
        UserProfileView.as_view(), 
        name='user_profile'
    ),

    # ========================================================================
    # 3. API Documentation Routes (Swagger / OpenAPI)
    # These routes are consumed by the frontend team for reference and debugging.
    # Base URL Prefix: /api/
    # ========================================================================

    # GET /api/schema/
    # Serves the machine-readable OpenAPI schema definition (JSON/YAML).
    path(
        'schema/', 
        SpectacularAPIView.as_view(), 
        name='schema'
    ),
    
    # GET /api/schema/swagger-ui/
    # Serves the interactive Swagger UI interface.
    path(
        'schema/swagger-ui/', 
        SpectacularSwaggerView.as_view(url_name='schema'), 
        name='swagger-ui'
    ),

    # Optional: Redoc Interface
    # GET /api/schema/redoc/
    # path(
    #     'schema/redoc/', 
    #     SpectacularRedocView.as_view(url_name='schema'), 
    #     name='redoc'
    # ),
]