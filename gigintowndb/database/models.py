from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, account_type, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, account_type=account_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, account_type, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, account_type, password, **extra_fields)

class Event(models.Model):
    EventID = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=255, null=False)
    Flyer = models.TextField(max_length=3000, null=True)
    Description = models.TextField(max_length=1000, null=False)
    Artists = models.CharField(max_length=255, null=False)
    Date = models.CharField(max_length=20, null=False)
    Time = models.TimeField(null=True)
    Address = models.CharField(max_length=255, null=False, default='Default Address')
    City = models.CharField(max_length=255, null=False, default='Default City')
    State = models.CharField(max_length=255, null=False, default='Default State')
    ZipCode = models.CharField(max_length=255, null=False, default=12345)
    Venue = models.CharField(max_length=255, null=False)
    Price = models.CharField(max_length=255, null=True)
    IsAllAges = models.BooleanField(null=False)
    Link = models.TextField(max_length=2000, null=True, blank='True')
    Created_By_Email = models.CharField(max_length=255, null=False, default='user@user.com')

    def __str__(self):
        return self.Title
    
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    account_type = models.CharField(max_length=20, null=True)
    saved_events = models.ManyToManyField(Event, related_name='users_who_saved', blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    zipCode = models.CharField(max_length=255, null=True, blank=True)
    businessName = models.CharField(max_length=255, null =True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['account_type']

    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)

    class Meta(AbstractUser.Meta):
        ordering = ["-date_joined"]
        db_table = "users"