"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):  # method overridden
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):  # method overridden
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

# serializer parse incoming json data into python dict data and check if
# these data match those requirenemt in Meta class before passing it down to validate_data


# can i say the fields exist to confirm those 3 input are provided when creating a user?
# -----------------------------------------------------------------------------------------
# The fields attribute in the Meta class of the UserSerializer specifies the
# fields that need to be provided when creating a user. If any of these fields
# ('email', 'password', 'name' in your case) are missing in the incoming data
# during deserialization (like when handling a POST request), Django's serializers
# will raise a validation error.

# the instance and validated_data parameters are automatically passed to the update()
# method when you perform an update operation using the serializer.




class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):    # pw is not hashed here in the attrs and method overridden
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

# the sequence of validation in Django REST Framework
# -----------------------------------------------------------------------------------------
# Field-level validation: The serializer's defined fields
# (serializers.EmailField(), serializers.CharField(), etc.)
# validate the input data. If any of these validations fail,
# a ValidationError is raised and the process stops here.

# validate_<fieldname> methods: If you have any methods in
# the serializer named validate_<fieldname>, these are called
# next for additional field-level validation.

# validate method: If field-level validation passes, the serializer's
# validate method is called for object-level validation. You can override
# this method for custom validation that requires access to multiple fields,
# as in your AuthTokenSerializer.


# can i say Serializer is to handle every post request with json data posted?
# -----------------------------------------------------------------------------------------
# Serializers in Django REST Framework are used to handle JSON data for incoming
# HTTP requests like POST and PUT, and also to format models into JSON for HTTP responses.
# They serve as a validation layer for incoming data and a transformation layer for outgoing data.