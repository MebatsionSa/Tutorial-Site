from django.db import models

# Create your models here.
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from django.utils.timezone import now

class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, password=None):
        """
        Creates and saves a User with the givem email, date_of_birth, registration_date, and password """
        if not email:
            raise ValueError('Users must have an email address.')
        
        user = self.model(
            username=username.lower(),
            first_name=first_name.title(),
            last_name=last_name.title(),
            email=self.normalize_email(email),
            registration_date=timezone.now().date(),
            #date_of_birth = date_of_birth,
        )
        user.set_password(password)
        user.is_anonymous= False
        user.save(using=self._db)
        return user

    def create_superuser(self,username, first_name, last_name, email, password):
        """
        Creates and saves a superuser with the givem email, date_of_birth, registration_date, and password 
        """
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(
        verbose_name='username',
        max_length=255, 
        unique=True,
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255, 
        unique=True,
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    registration_date = models.DateField(default=now)
    #date_of_birth = models.DateField(default=now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    #is_anonymous = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    """
    def __str__(self):
        return self.email
    """
    def get_all_permissions(obj=None):
        if obj.is_superuser:
            return True
        return False

    def get_user_permissions(self,obj=None):
        if obj.is_active:
            return True
        return False

    def has_perm(self, perm, obj=None):
        # superuser is True
        return True
        
    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        return False
    
    @property
    def is_staff(self):
        return self.is_admin
