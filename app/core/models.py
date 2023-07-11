"""
Database models.
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'
    # the str is created below in the appropriate format for the operating system that we're running the code on
    return os.path.join('uploads', 'recipe', filename)

class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    # reserved name for this method
    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

# User and UserManager are reserved?
# who provides the model class and what is this looks like? dose it provides set_password and save?
# is the model in user = self.model(email=self.normalize_email(email), **extra_fields) provided by BaseUserManager?

# !!!
# the convention is to name the default manager for a model as objects.
# By assigning the UserManager instance to the objects attribute of the User model,
# it becomes the default manager for the User model.

# you can create an instance of the UserManager class and assign
# it to a variable like obj = UserManager() instead of assigning it to the objects
# attribute of the User model

# self.model(email=self.normalize_email(email), **extra_fields)
# is equivalent to user = User(email=self.normalize_email(email), **extra_fields).

class Recipe(models.Model):
    """Recipe object."""
    user = models.ForeignKey(            # ForeignKey sets up the relationship with another model
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)  # optional
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)  # optional
    tags = models.ManyToManyField('Tag')   # optional
    ingredients = models.ManyToManyField('Ingredient')   # optional
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)  # optional
    # When Django calls the function specified in upload_to, it automatically provides \
    # the instance and filename arguments.
    # The uploaded image will be saved to the path returned by the recipe_image_file_path function.

    def __str__(self):
        return self.title

class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient for recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
# if you have a Recipe object, you can get all its tags by calling recipe.tags.all().
# Similarly, you can get all recipes that a particular tag is associated with by calling tag.recipe_set.all().
# recipe_set is the default related name Django creates for the reverse lookup from Tag to Recipe.
