from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Inherits fields like username, email (overridden below), password, first_name, last_name
    
    # Override to enforce shorter, explicit limits for profile display fields.
    first_name = models.CharField(max_length=50, blank=True, verbose_name="First Name")
    last_name = models.CharField(max_length=50, blank=True, verbose_name="Last Name")

    # === Core B2B Advisor Identity Fields ===
    
    # Unique ID linking the advisor to specific FUND_CODEs for access control.
    advisor_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Advisor ID"
    )
    
    # The firm or accounting practice the advisor belongs to.
    firm_name = models.CharField(
        max_length=150, 
        blank=True, 
        db_index=True,
        verbose_name="Firm/Company Name"
    )
    
    # The role within the external firm (e.g., Senior SMSF Advisor).
    role = models.CharField(
        max_length=100, 
        blank=True, 
        default="Financial Advisor",
        verbose_name="Role in Firm"
    )

    # === Profile Display Fields ===
    bio = models.TextField(blank=True)
    avatar_url = models.URLField(
        blank=True, 
        default="https://ui-avatars.com/api/?name=User", 
        verbose_name="Avatar URL"
    )

    # Enforce email uniqueness for secure B2B identity (overrides default AbstractUser behavior)
    email = models.EmailField(unique=True) 

    def __str__(self):
        # Human-readable representation for Django Admin
        return f"{self.username} ({self.advisor_id or self.email})"
