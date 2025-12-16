"""
URL configuration for the integra_core project (The Main Router).

This file defines the top-level routing for the entire application, serving three primary purposes:
1. Handles the root URL ('/') by redirecting users to the API documentation.
2. Sets up the default Django administrative interface ('/admin/').
3. Includes all application-level API endpoints defined in users.urls under the '/api/' prefix.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView 

# Note: Specific API views (like TokenObtainPairView or SpectacularAPIView) are 
# now imported and defined only in the application's urls.py (users/urls.py) 
# to keep the core router clean.

urlpatterns = [
    # 1. Root Path Handling: Redirects the base URL to the Swagger documentation.
    # This solves the 404 error when users visit http://127.0.0.1:8000/
    path(
        '', 
        RedirectView.as_view(url='/api/schema/swagger-ui/', permanent=True), 
        name='root_redirect'
    ), 
    
    # 2. Django Admin Interface
    path('admin/', admin.site.urls),
    
    # 3. API Entry Point: Includes all application-specific API routes (from users/urls.py).
    # All endpoints are now accessible under the /api/ prefix (e.g., /api/auth/login/).
    path('api/', include('users.urls')), 
]