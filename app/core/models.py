from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):

# **extra_fields : add any additional fields
    def create_user(self, email, password=None, **extra_fields ):
        #create and save a new USER
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # password is always encrypted, not stored in clear text
        user.set_password(password)
        user.save(using=self._db)

        return user

class User(AbstractBaseUser,PermissionsMixin):
    #Custom user model that supports using email instead of username
    email = models.EmailField(max_length = 255, unique = True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default = False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
