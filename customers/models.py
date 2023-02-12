from django.db import models
from PriceAnalysis.models import Holding
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class AccountManager(BaseUserManager):

    def create_user(self, address, username, password=None):
        if not address:
            raise ValueError("You need an ETH address for login")
        if not username:
            raise ValueError("You need an username")
        user = self.model(
            username=username,
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, address, username, password=None):
        user = self.create_user(
            address=address,
            username=username,
            password=password,
            )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    User using the app.
    """
    created_at = models.DateTimeField(verbose_name="created at", auto_now=False, auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)

    address = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=30, unique=True)

    holdings = models.ManyToManyField(Holding)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["address"]

    def __str__(self):
        return self.address

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def has_add_permission(self, request, obj=None):
        return False
