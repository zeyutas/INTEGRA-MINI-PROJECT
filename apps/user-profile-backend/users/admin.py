from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# === Custom Admin for B2B Advisor User ===

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Fieldsets for editing an EXISTING user
    fieldsets = UserAdmin.fieldsets + (
        # New section for B2B Advisor specific fields
        ('B2B Advisor Info', {'fields': ('advisor_id', 'firm_name', 'role', 'bio', 'avatar_url')}),
    )

    # Fieldsets for CREATING a NEW user
    add_fieldsets = UserAdmin.add_fieldsets + (
        # We need to explicitly define the fields here as well
        ('B2B Advisor Info', {
            'fields': ('advisor_id', 'firm_name', 'role', 'bio', 'avatar_url', 'email'),
        }),
    )

    # Optional: Display advisor_id and firm_name directly in the list view
    list_display = UserAdmin.list_display + ('advisor_id', 'firm_name', 'role')

# Note: The code is now clean, and the fields are logically grouped 
# in the Django Admin interface.