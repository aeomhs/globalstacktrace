from django.db import models
from django.contrib.auth.models import (
    # https://docs.djangoproject.com/en/2.2/topics/auth/customizing/
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone
from multiselectfield import MultiSelectField


class MyUserManager(BaseUserManager):
    def create_user(self, name, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not name:
            raise ValueError('Users must have a name')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            name=name,
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            name,
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# User
class MyUser(AbstractBaseUser):
    name = models.CharField(max_length=30)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'date_of_birth']

    # Created & Updated Time
    # https://stackoverflow.com/questions/3429878/automatic-creation-date-for-django-model-form-objects
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(MyUser, self).save(*args, **kwargs)


# Card
class Card(models.Model):
    # SKILL CHOICES
    pl_c = 'C'
    pl_java = 'JAVA'
    pl_python = 'PYTHON'
    PL_TYPE_CHOICES = (
        (pl_c, 'C'),
        (pl_java, 'JAVA'),
        (pl_python, 'PYTHON'),
    )

    # User_Card
    # One to One
    owner = models.OneToOneField(
        MyUser, 
        on_delete=models.CASCADE, 
        primary_key=True,
    ) 
    
    homepage = models.URLField()
    summary = models.CharField(max_length=50, null=True)
    skill = MultiSelectField(
        'skill',
        max_choices=3,
        choices=PL_TYPE_CHOICES,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.owner)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if self.created_at is None:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Card, self).save(*args, **kwargs)


# Project
class Project(models.Model):
    card = models.ForeignKey(
        Card, 
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length = 30)
    link = models.URLField()

    def __str__(self):
        return str(self.card)+" : "+str(self.name)


#  Certification
class Certification(models.Model):
    # CHOICES
    license_type = 'LCS'
    award_type = 'AWD'
    certificate_type = 'CTF'
    CERTIFICATION_TYPE_CHOICES = (
        (license_type, '자격증'),
        (award_type, '수상 내역'),
        (certificate_type, '수료증'),
    )
    
    card = models.ForeignKey(
        Card, 
        on_delete=models.CASCADE,
    )

    date = models.DateField()
    name = models.CharField('name', max_length=20)
    certificate_type = models.CharField(
        'type', 
        max_length=3, 
        choices=CERTIFICATION_TYPE_CHOICES,
    )
    organization = models.CharField(max_length=20)

    def __str__(self):
        return str(self.card)+" : "+str(self.name)


# Like
class Like(models.Model):
    user = models.ForeignKey(
        MyUser, 
        on_delete=models.CASCADE,
    )

    liked = models.ForeignKey(
        Card, 
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.user)+" likes "+str(self.liked)
